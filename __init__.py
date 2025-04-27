def classFactory(iface):
    from .plugin import OAuth2ClientCredentialsPlugin
    return OAuth2ClientCredentialsPlugin(iface)
