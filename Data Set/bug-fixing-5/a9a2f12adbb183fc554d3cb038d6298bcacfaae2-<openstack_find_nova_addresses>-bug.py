def openstack_find_nova_addresses(addresses, ext_tag, key_name=None):
    ret = []
    for (k, v) in addresses.iteritems():
        if (key_name and (k == key_name)):
            ret.extend([addrs['addr'] for addrs in v])
        else:
            for interface_spec in v:
                if (('OS-EXT-IPS:type' in interface_spec) and (interface_spec['OS-EXT-IPS:type'] == ext_tag)):
                    ret.append(interface_spec['addr'])
    return ret