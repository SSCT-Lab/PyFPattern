

def main():
    module = AnsibleModule(argument_spec=dict(repo=dict(required=True), user=dict(required=True), token=dict(required=True, no_log=True), action=dict(required=True, choices=['latest_release'])), supports_check_mode=True)
    if (not HAS_GITHUB_API):
        module.fail_json(msg='Missing requried github3 module (check docs or install with: pip install github3)')
    repo = module.params['repo']
    user = module.params['user']
    login_token = module.params['token']
    action = module.params['action']
    try:
        gh = github3.login(token=str(login_token))
        gh.me()
    except github3.AuthenticationFailed:
        e = get_exception()
        module.fail_json(msg=('Failed to connect to Github: %s' % e))
    repository = gh.repository(str(user), str(repo))
    if (not repository):
        module.fail_json(msg=("Repository %s/%s doesn't exist" % (user, repo)))
    if (action == 'latest_release'):
        release = repository.latest_release()
        if release:
            module.exit_json(tag=release.tag_name)
        else:
            module.exit_json(tag=None)
