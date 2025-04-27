# QGIS OAuth2 Client Credentials Plugin

This QGIS plugin allows you to authenticate WFS, WMS, or other HTTP-based services using OAuth2 **Client Credentials Grant** flow.

It automatically:
- Retrieves an access token.
- Refreshes tokens as needed.
- Configures a QGIS Authentication configuration (APIHeader method) with the valid token.

## ✨ Features

- OAuth2 Client Credentials authentication.
- Secure storage of client secret using QGIS Authentication Database.
- Easy-to-use configuration dialog.
- Remember your settings between QGIS sessions.
- Toggle visibility of the client secret field (👁️).

## 🛠 Installation

1. Download or clone this repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/qgis-oauth2-client-credentials-plugin.git
