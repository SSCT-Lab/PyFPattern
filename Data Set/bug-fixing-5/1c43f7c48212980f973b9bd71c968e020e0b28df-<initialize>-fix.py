def initialize():
    '\n    This function initializes the FreeIPA/IPA API. This function requires\n    no arguments. A kerberos key must be present in the users keyring in\n    order for this to work. IPA default configuration directory is /etc/ipa,\n    this path could be overridden with IPA_CONFDIR environment variable.\n    '
    api.bootstrap(context='cli')
    if (not os.path.isdir(api.env.confdir)):
        print(('WARNING: IPA configuration directory (%s) is missing. Environment variable IPA_CONFDIR could be used to override default path.' % api.env.confdir))
    if (LooseVersion(IPA_VERSION) >= LooseVersion('4.6.2')):
        if (('server' not in api.env) or ('domain' not in api.env)):
            sys.exit(("ERROR: ('jsonrpc_uri' or 'xmlrpc_uri') or 'domain' are not defined in '[global]' section of '%s' nor in '%s'." % (api.env.conf, api.env.conf_default)))
    api.finalize()
    try:
        api.Backend.rpcclient.connect()
    except AttributeError:
        api.Backend.xmlclient.connect()
    return api