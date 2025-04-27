from qgis.PyQt.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QPushButton, QHBoxLayout
from qgis.PyQt.QtCore import QSettings
from qgis.core import QgsAuthMethodConfig, QgsApplication

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configure OAuth2 Client Credentials")
        self.setMinimumSize(500, 300)

        layout = QFormLayout(self)

        self.client_id = QLineEdit(self)
        self.client_secret = QLineEdit(self)
        self.client_secret.setEchoMode(QLineEdit.Password)
        self.toggle_password_button = QPushButton("👁")
        self.toggle_password_button.setCheckable(True)
        self.toggle_password_button.toggled.connect(self.toggle_password_visibility)

        secret_layout = QHBoxLayout()
        secret_layout.addWidget(self.client_secret)
        secret_layout.addWidget(self.toggle_password_button)

        self.scope = QLineEdit(self)
        self.auth_url = QLineEdit(self)
        self.resource = QLineEdit(self)

        settings = QSettings()
        self.client_id.setText(settings.value("oauth2_client_id", ""))
        self.scope.setText(settings.value("oauth2_scope", "gipod_pdo_read"))
        self.auth_url.setText(settings.value("oauth2_auth_url", "https://authenticatie-ti.vlaanderen.be/op/v1/token"))
        self.resource.setText(settings.value("oauth2_resource", "https://gipod.api.test-vlaanderen.be/synductis/wfs"))
        self.client_secret.setText(settings.value("oauth2_client_secret", ""))

        layout.addRow("Client ID", self.client_id)
        layout.addRow("Client Secret", secret_layout)
        layout.addRow("Scopes", self.scope)
        layout.addRow("Auth URL", self.auth_url)
        layout.addRow("Resource URL", self.resource)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def toggle_password_visibility(self, checked):
        self.client_secret.setEchoMode(QLineEdit.Normal if checked else QLineEdit.Password)


