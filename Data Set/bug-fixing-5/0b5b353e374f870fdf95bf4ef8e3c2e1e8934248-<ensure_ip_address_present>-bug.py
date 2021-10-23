def ensure_ip_address_present(nb_endpoint, data):
    "\n    :returns dict(ip_address, msg, changed): dictionary resulting of the request,\n    where 'ip_address' is the serialized ip fetched or newly created in Netbox\n    "
    if (not isinstance(data, dict)):
        changed = False
        return {
            'msg': data,
            'changed': changed,
        }
    try:
        ip_addr = _search_ip(nb_endpoint, data)
    except ValueError:
        return _error_multiple_ip_results(data)
    if (not ip_addr):
        return create_ip_address(nb_endpoint, data)
    else:
        ip_addr = ip_addr.serialize()
        changed = False
        msg = ('IP Address %s already exists' % data['address'])
        return {
            'ip_address': ip_addr,
            'msg': msg,
            'changed': changed,
        }