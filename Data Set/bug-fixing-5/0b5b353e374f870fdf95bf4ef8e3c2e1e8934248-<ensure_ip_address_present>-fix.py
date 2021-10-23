def ensure_ip_address_present(nb_endpoint, data):
    "\n    :returns dict(ip_address, msg, changed): dictionary resulting of the request,\n    where 'ip_address' is the serialized ip fetched or newly created in Netbox\n    "
    if (not isinstance(data, dict)):
        changed = False
        return {
            'msg': data,
            'changed': changed,
        }
    try:
        nb_addr = _search_ip(nb_endpoint, data)
    except ValueError:
        return _error_multiple_ip_results(data)
    result = {
        
    }
    if (not nb_addr):
        return create_ip_address(nb_endpoint, data)
    else:
        (ip_addr, diff) = update_netbox_object(nb_addr, data, module.check_mode)
        if (ip_addr is False):
            module.fail_json(msg=("Request failed, couldn't update IP: %s" % data['address']))
        if diff:
            msg = ('IP Address %s updated' % data['address'])
            changed = True
            result['diff'] = diff
        else:
            ip_addr = nb_addr.serialize()
            changed = False
            msg = ('IP Address %s already exists' % data['address'])
        return {
            'ip_address': ip_addr,
            'msg': msg,
            'changed': changed,
        }