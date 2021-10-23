def service_identical(client, module, service_proxy):
    service_list = service.get_filtered(client, ('name:%s' % module.params['name']))
    diff_dict = service_proxy.diff_object(service_list[0])
    if ('ip' in diff_dict):
        del diff_dict['ip']
    if (len(diff_dict) == 0):
        return True
    else:
        return False