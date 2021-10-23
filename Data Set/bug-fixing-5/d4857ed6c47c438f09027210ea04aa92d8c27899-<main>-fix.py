def main():
    module = AnsibleModule(argument_spec=dict(repo=dict(required=True), user=dict(required=True), password=dict(no_log=True), token=dict(no_log=True), action=dict(required=True, choices=['latest_release'])), supports_check_mode=True, required_one_of=(('password', 'token'),), mutually_exclusive=(('password', 'token'),))
    if (not HAS_GITHUB_API):
        module.fail_json(msg='Missing required github3 module (check docs or install with: pip install github3.py==1.0.0a4)')
    repo = module.params['repo']
    user = module.params['user']
    password = module.params['password']
    login_token = module.params['token']
    action = module.params['action']
    try:
        if (user and password):
            gh_obj = github3.login(user, password=password)
        elif login_token:
            gh_obj = github3.login(token=login_token)
        gh_obj.me()
    except github3.AuthenticationFailed:
        e = get_exception()
        module.fail_json(msg=('Failed to connect to GitHub: %s' % e), details=('Please check username and password or token for repository %s' % repo))
    repository = gh_obj.repository(user, repo)
    if (not repository):
        module.fail_json(msg=("Repository %s/%s doesn't exist" % (user, repo)))
    if (action == 'latest_release'):
        release = repository.latest_release()
        if release:
            module.exit_json(tag=release.tag_name)
        else:
            module.exit_json(tag=None)