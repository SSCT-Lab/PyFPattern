

def main():
    module = AnsibleModule(argument_spec=dict(server_url=dict(required=True, type='str'), validate_certs=dict(required=False, default=True, type='bool', aliases=['verify_ssl']), login_user=dict(required=False, no_log=True, type='str'), login_password=dict(required=False, no_log=True, type='str'), login_token=dict(required=False, no_log=True, type='str'), name=dict(required=True, type='str'), path=dict(required=False, type='str'), description=dict(required=False, type='str'), state=dict(default='present', choices=['present', 'absent'])), mutually_exclusive=[['login_user', 'login_token'], ['login_password', 'login_token']], required_together=[['login_user', 'login_password']], required_one_of=[['login_user', 'login_token']], supports_check_mode=True)
    if (not HAS_GITLAB_PACKAGE):
        module.fail_json(msg='Missing requried gitlab module (check docs or install with: pip install python-gitlab')
    server_url = module.params['server_url']
    validate_certs = module.params['validate_certs']
    login_user = module.params['login_user']
    login_password = module.params['login_password']
    login_token = module.params['login_token']
    group_name = module.params['name']
    group_path = module.params['path']
    description = module.params['description']
    state = module.params['state']
    try:
        git = gitlab.Gitlab(url=server_url, ssl_verify=validate_certs, email=login_user, password=login_password, private_token=login_token, api_version=4)
        git.auth()
    except (gitlab.exceptions.GitlabAuthenticationError, gitlab.exceptions.GitlabGetError) as e:
        module.fail_json(msg=('Failed to connect to Gitlab server: %s' % to_native(e)))
    if (group_path is None):
        group_path = group_name.replace(' ', '_')
    group = GitLabGroup(module, git)
    group_name = group_name.lower()
    group_exists = group.existsGroup(group_name)
    if (group_exists and (state == 'absent')):
        if group.deleteGroup():
            module.exit_json(changed=True, result=('Successfully deleted group %s' % group_name))
    elif (state == 'absent'):
        module.exit_json(changed=False, result='Group deleted or does not exists')
    elif group.createOrUpdateGroup(name=group_name, path=group_path, description=description):
        module.exit_json(changed=True, result=('Successfully created or updated the group %s' % group_name))
    else:
        module.exit_json(changed=False, result=('No need to update the group %s' % group_name))
