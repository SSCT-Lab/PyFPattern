def set_password(module, ssid, api_url, user, pwd, current_password=None, new_password=None, set_admin=False):
    set_pass = ('storage-systems/%s/passwords' % ssid)
    url = (api_url + set_pass)
    if (not current_password):
        current_password = ''
    post_body = json.dumps(dict(currentAdminPassword=current_password, adminPassword=set_admin, newPassword=new_password))
    try:
        (rc, data) = request(url, method='POST', data=post_body, headers=HEADERS, url_username=user, url_password=pwd, ignore_errors=True)
    except Exception as e:
        module.fail_json(msg=('Failed to set system password. Id [%s].  Error [%s]' % (ssid, to_native(e))), exception=traceback.format_exc())
    if (rc == 422):
        post_body = json.dumps(dict(currentAdminPassword='', adminPassword=set_admin, newPassword=new_password))
        try:
            (rc, data) = request(url, method='POST', data=post_body, headers=HEADERS, url_username=user, url_password=pwd)
        except:
            module.fail_json(msg='Wrong or no admin password supplied. Please update your playbook and try again')
    update_data = update_storage_system_pwd(module, ssid, new_password, api_url, user, pwd)
    if (int(rc) == 204):
        return update_data
    else:
        module.fail_json(msg=('%s:%s' % (rc, data)))