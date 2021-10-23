

def _network_args(module, cloud):
    args = []
    nics = module.params['nics']
    if (not isinstance(nics, list)):
        module.fail_json(msg="The 'nics' parameter must be a list.")
    for net in _parse_nics(nics):
        if (not isinstance(net, dict)):
            module.fail_json(msg="Each entry in the 'nics' parameter must be a dict.")
        if net.get('net-id'):
            args.append(net)
        elif net.get('net-name'):
            by_name = cloud.get_network(net['net-name'])
            if (not by_name):
                module.fail_json(msg=('Could not find network by net-name: %s' % net['net-name']))
            args.append({
                'net-id': by_name['id'],
            })
        elif net.get('port-id'):
            args.append(net)
        elif net.get('port-name'):
            by_name = cloud.get_port(net['port-name'])
            if (not by_name):
                module.fail_json(msg=('Could not find port by port-name: %s' % net['port-name']))
            args.append({
                'port-id': by_name['id'],
            })
    return args
