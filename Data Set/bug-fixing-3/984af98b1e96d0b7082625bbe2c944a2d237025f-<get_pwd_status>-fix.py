def get_pwd_status(module, ssid, api_url, user, pwd):
    pwd_status = ('storage-systems/%s/passwords' % ssid)
    url = (api_url + pwd_status)
    try:
        (rc, data) = request(url, headers=HEADERS, url_username=user, url_password=pwd, validate_certs=module.validate_certs)
        return (data['readOnlyPasswordSet'], data['adminPasswordSet'])
    except HTTPError as e:
        module.fail_json(msg=('There was an issue with connecting, please check that your endpoint is properly defined and your credentials are correct: %s' % to_native(e)))