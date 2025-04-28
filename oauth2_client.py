from qgis.PyQt.QtCore import QObject, QTimer, QDateTime
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import QgsMessageLog, Qgis, QgsAuthMethodConfig, QgsApplication
import requests

class OAuth2ClientCredentials(QObject):
    def __init__(self, auth_url, client_id, client_secret, scope=None, resource=None):
        super().__init__()
        self.auth_url = auth_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.resource = resource
        self.token = None
        self.token_type = "Bearer"
        self.token_expiry = None
        self.token_expires_in = 3600
        self.token_timer = QTimer()
        self.token_timer.timeout.connect(self.check_token_validity)
        self.token_requested = False

    def log_debug(self, message):
        QgsMessageLog.logMessage(message, "OAuth2ClientCredentials", Qgis.Info)

    def log_error(self, message):
        QgsMessageLog.logMessage(message, "OAuth2ClientCredentials", Qgis.Critical)
        QMessageBox.critical(None, "OAuth2 Authentication Error", message)

    def get_token(self):
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        if self.scope:
            data['scope'] = self.scope
        if self.resource:
            data['resource'] = self.resource

        try:
            response = requests.post(self.auth_url, data=data)
            response.raise_for_status()
            token_data = response.json()
            self.token = token_data['access_token']
            self.token_type = token_data.get('token_type', 'Bearer')
            self.token_expires_in = token_data.get('expires_in', 3600)
            self.token_expiry = QDateTime.currentDateTimeUtc().addSecs(self.token_expires_in - 60)
            self.token_timer.start(30000)
            self.log_debug(f"Token obtained successfully, expires in {self.token_expires_in} seconds.")
            self.token_requested = True
            self.create_or_update_authentication_config()
            return self.token
        except Exception as e:
            self.log_error(f"Failed to get token: {str(e)}")
            raise

    def check_token_validity(self):
        if self.token_expiry and QDateTime.currentDateTimeUtc() >= self.token_expiry:
            self.log_debug("Token expired, refreshing...")
            self.get_token()

    def create_or_update_authentication_config(self):
        try:
            auth_manager = QgsApplication.authManager()
            config_ids = auth_manager.availableAuthMethodConfigs()
            existing_configs = []

            for cfg_id in config_ids:
                cfg = QgsAuthMethodConfig()
                auth_manager.loadAuthenticationConfig(cfg_id, cfg)
                if cfg.isValid() and cfg.name() == "GIPOD Authenticatie" and cfg.method() == "APIHeader":
                    existing_configs.append(cfg)

            if existing_configs:
                keep_cfg = existing_configs[0]
                for duplicate_cfg in existing_configs[1:]:
                    auth_manager.removeAuthenticationConfig(duplicate_cfg.id())
                    self.log_debug(f"Removed duplicate authentication configuration with ID {duplicate_cfg.id()}.")

                if keep_cfg.isValid():
                    keep_cfg.setConfig("Authorization", f"Bearer {self.token}")
                    auth_manager.updateAuthenticationConfig(keep_cfg)
                    self.log_debug("Authentication configuration updated with refreshed token.")
            else:
                authcfg = QgsAuthMethodConfig("APIHeader")
                authcfg.setName("GIPOD Authenticatie")
                authcfg.setUri(self.resource)
                authcfg.setConfig("Authorization", f"Bearer {self.token}")
                auth_manager.storeAuthenticationConfig(authcfg)
                self.log_debug("Authentication configuration 'GIPOD Authenticatie' created successfully.")

        except Exception as e:
            self.log_error(f"Failed to create or update authentication configuration: {str(e)}")
