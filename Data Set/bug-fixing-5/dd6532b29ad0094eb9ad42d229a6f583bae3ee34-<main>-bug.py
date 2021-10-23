def main():
    global user_id
    module = AnsibleModule(argument_spec=dict(server_url=dict(required=True), validate_certs=dict(required=False, default=True, type='bool', aliases=['verify_ssl']), login_user=dict(required=False, no_log=True), login_password=dict(required=False, no_log=True), login_token=dict(required=False, no_log=True), name=dict(required=True), username=dict(required=True), password=dict(required=True, no_log=True), email=dict(required=True), sshkey_name=dict(required=False), sshkey_file=dict(required=False), group=dict(required=False), access_level=dict(required=False, choices=['guest', 'reporter', 'developer', 'master', 'owner']), state=dict(default='present', choices=['present', 'absent']), confirm=dict(required=False, default=True, type='bool')), supports_check_mode=True)
    if (not HAS_GITLAB_PACKAGE):
        module.fail_json(msg='Missing required gitlab module (check docs or install with: pip install pyapi-gitlab')
    server_url = module.params['server_url']
    verify_ssl = module.params['validate_certs']
    login_user = module.params['login_user']
    login_password = module.params['login_password']
    login_token = module.params['login_token']
    user_name = module.params['name']
    user_username = module.params['username']
    user_password = module.params['password']
    user_email = module.params['email']
    user_sshkey_name = module.params['sshkey_name']
    user_sshkey_file = module.params['sshkey_file']
    group_name = module.params['group']
    access_level = module.params['access_level']
    state = module.params['state']
    confirm = module.params['confirm']
    if ((login_user is not None) and (login_password is not None)):
        use_credentials = True
    elif (login_token is not None):
        use_credentials = False
    else:
        module.fail_json(msg='No login credentials are given. Use login_user with login_password, or login_token')
    if ((user_sshkey_file is not None) and (user_sshkey_name is not None)):
        use_sshkey = True
    else:
        use_sshkey = False
    if ((group_name is not None) and (access_level is not None)):
        add_to_group = True
        group_name = group_name.lower()
    else:
        add_to_group = False
    user_username = user_username.lower()
    try:
        if use_credentials:
            git = gitlab.Gitlab(host=server_url, verify_ssl=verify_ssl)
            git.login(user=login_user, password=login_password)
        else:
            git = gitlab.Gitlab(server_url, token=login_token, verify_ssl=verify_ssl)
    except Exception as e:
        module.fail_json(msg=('Failed to connect to Gitlab server: %s ' % to_native(e)))
    auth_msg = git.currentuser().get('message', None)
    if ((auth_msg is not None) and (auth_msg == '401 Unauthorized')):
        module.fail_json(msg='User unauthorized', details='User is not allowed to access Gitlab server using login_token. Please check login_token')
    user = GitLabUser(module, git)
    if ((not user.existsUser(user_username)) and (state == 'absent')):
        module.exit_json(changed=False, result='User already deleted or does not exists')
    elif (state == 'absent'):
        user.deleteUser(user_username)
    else:
        user.createOrUpdateUser(user_name, user_username, user_password, user_email, user_sshkey_name, user_sshkey_file, group_name, access_level, confirm)