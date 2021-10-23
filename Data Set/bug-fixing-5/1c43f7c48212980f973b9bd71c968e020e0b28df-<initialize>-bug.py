def initialize():
    '\n    This function initializes the FreeIPA/IPA API. This function requires\n    no arguments. A kerberos key must be present in the users keyring in\n    order for this to work.\n    '
    api.bootstrap(context='cli')
    api.finalize()
    try:
        api.Backend.rpcclient.connect()
    except AttributeError:
        api.Backend.xmlclient.connect()
    return api