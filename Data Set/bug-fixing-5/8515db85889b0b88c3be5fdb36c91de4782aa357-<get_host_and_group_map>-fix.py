def get_host_and_group_map(module, ssid, api_url, user, pwd, validate_certs):
    mapping = dict(host=dict(), group=dict())
    hostgroups = ('storage-systems/%s/host-groups' % ssid)
    groups_url = (api_url + hostgroups)
    try:
        (hg_rc, hg_data) = request(groups_url, headers=HEADERS, url_username=user, url_password=pwd, validate_certs=validate_certs)
    except:
        err = get_exception()
        module.fail_json(msg=('Failed to get host groups. Id [%s]. Error [%s]' % (ssid, str(err))))
    for group in hg_data:
        mapping['group'][group['name']] = group['id']
    hosts = ('storage-systems/%s/hosts' % ssid)
    hosts_url = (api_url + hosts)
    try:
        (h_rc, h_data) = request(hosts_url, headers=HEADERS, url_username=user, url_password=pwd, validate_certs=validate_certs)
    except:
        err = get_exception()
        module.fail_json(msg=('Failed to get hosts. Id [%s]. Error [%s]' % (ssid, str(err))))
    for host in h_data:
        mapping['host'][host['name']] = host['id']
    return mapping