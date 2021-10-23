

def get_resource_connection(module):
    if hasattr(module, '_connection'):
        return module._connection
    capabilities = get_capabilities(module)
    network_api = capabilities.get('network_api')
    if (network_api in ('cliconf', 'nxapi', 'eapi')):
        module._connection = Connection(module._socket_path)
    elif (network_api == 'netconf'):
        module._connection = NetconfConnection(module._socket_path)
    else:
        module.fail_json(msg='Invalid connection type {0!s}'.format(network_api))
    return module._connection
