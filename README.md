# QGIS OAuth2 Client Credentials Plugin

This QGIS plugin allows you to authenticate WFS, WMS, or other HTTP-based services using OAuth2 **Client Credentials Grant** flow.

The plugin was written to facilitate authentication for the GIPOD secured ogc services. It refers to GIPOD, but should work for other data sources that are secured using OAuth2 CCG.

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

