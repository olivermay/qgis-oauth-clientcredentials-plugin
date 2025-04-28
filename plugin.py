from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsApplication
from .oauth2_client import OAuth2ClientCredentials
from .settings_dialog import SettingsDialog

class OAuth2ClientCredentialsPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.oauth_client = None
        self.action = None

    def initGui(self):
        self.action = QAction("GIPOD CCG Authenticatie", self.iface.mainWindow())
        self.action.triggered.connect(self.create_authentication)
        self.iface.addPluginToMenu("&GIPOD Auth", self.action)
        self.iface.addToolBarIcon(self.action)

    def create_authentication(self):
        dialog = SettingsDialog()
        if dialog.exec_():
            settings = QSettings()
            settings.setValue("oauth2_client_id", dialog.client_id.text())
            settings.setValue("oauth2_scope", dialog.scope.text())
            settings.setValue("oauth2_auth_url", dialog.auth_url.text())
            settings.setValue("oauth2_resource", dialog.resource.text())
            # Warning! client secret is stored in settings unencrypted
            settings.setValue("oauth2_authcfg_id", dialog.client_secret.text())

            self.oauth_client = OAuth2ClientCredentials(
                auth_url=dialog.auth_url.text(),
                client_id=dialog.client_id.text(),
                client_secret=dialog.client_secret.text(),
                scope=dialog.scope.text(),
                resource=dialog.resource.text()
            )
            self.oauth_client.get_token()

    def unload(self):
        if self.action:
            self.iface.removePluginMenu("&GIPOD Auth", self.action)
            self.iface.removeToolBarIcon(self.action)
