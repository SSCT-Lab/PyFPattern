def get_hostgroups(module, ssid, api_url, user, pwd, validate_certs):
    groups = ('storage-systems/%s/host-groups' % ssid)
    url = (api_url + groups)
    try:
        (rc, data) = request(url, headers=HEADERS, url_username=user, url_password=pwd, validate_certs=validate_certs)
        return data
    except Exception:
        module.fail_json(msg='There was an issue with connecting, please check that yourendpoint is properly defined and your credentials are correct')