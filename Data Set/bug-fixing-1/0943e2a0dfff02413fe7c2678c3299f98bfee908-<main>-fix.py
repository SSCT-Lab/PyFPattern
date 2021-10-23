

def main():
    module = AnsibleModule(argument_spec=dict(repository=dict(type='str', required=True, aliases=['repo']), url=dict(type='str', required=True), content_type=dict(type='str', choices=('json', 'form'), required=False, default='form'), secret=dict(type='str', required=False, no_log=True), insecure_ssl=dict(type='bool', required=False, default=False), events=dict(type='list', elements='str', required=False), active=dict(type='bool', required=False, default=True), state=dict(type='str', required=False, choices=('absent', 'present'), default='present'), user=dict(type='str', required=True), password=dict(type='str', required=False, no_log=True), token=dict(type='str', required=False, no_log=True), github_url=dict(type='str', required=False, default='https://api.github.com')), mutually_exclusive=(('password', 'token'),), required_one_of=(('password', 'token'),), required_if=(('state', 'present', ('events',)),))
    if (not HAS_GITHUB):
        module.fail_json(msg=missing_required_lib('PyGithub'), exception=GITHUB_IMP_ERR)
    try:
        github_conn = github.Github(module.params['user'], (module.params.get('password') or module.params.get('token')), base_url=module.params['github_url'])
    except github.GithubException as err:
        module.fail_json(msg=('Could not connect to GitHub at %s: %s' % (module.params['github_url'], to_native(err))))
    try:
        repo = github_conn.get_repo(module.params['repository'])
    except github.BadCredentialsException as err:
        module.fail_json(msg=('Could not authenticate to GitHub at %s: %s' % (module.params['github_url'], to_native(err))))
    except github.UnknownObjectException as err:
        module.fail_json(msg=('Could not find repository %s in GitHub at %s: %s' % (module.params['repository'], module.params['github_url'], to_native(err))))
    except Exception as err:
        module.fail_json(msg=('Could not fetch repository %s from GitHub at %s: %s' % (module.params['repository'], module.params['github_url'], to_native(err))), exception=traceback.format_exc())
    hook = None
    try:
        for hook in repo.get_hooks():
            if (hook.config.get('url') == module.params['url']):
                break
        else:
            hook = None
    except github.GithubException as err:
        module.fail_json(msg=('Unable to get hooks from repository %s: %s' % (module.params['repository'], to_native(err))))
    changed = False
    data = {
        
    }
    if ((hook is None) and (module.params['state'] == 'present')):
        (changed, data) = create_hook(repo, module)
    elif ((hook is not None) and (module.params['state'] == 'absent')):
        try:
            hook.delete()
        except github.GithubException as err:
            module.fail_json(msg=('Unable to delete hook from repository %s: %s' % (repo.full_name, to_native(err))))
        else:
            changed = True
    elif ((hook is not None) and (module.params['state'] == 'present')):
        (changed, data) = update_hook(repo, hook, module)
    module.exit_json(changed=changed, **data)
