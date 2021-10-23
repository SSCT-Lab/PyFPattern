def main():
    argument_spec = basic_auth_argument_spec()
    argument_spec.update(dict(api_token=dict(type='str', no_log=True), state=dict(type='str', default='present', choices=['absent', 'present']), project=dict(type='str', required=True), hook_url=dict(type='str', required=True), push_events=dict(type='bool', default=True), push_events_branch_filter=dict(type='str', default=''), issues_events=dict(type='bool', default=False), merge_requests_events=dict(type='bool', default=False), tag_push_events=dict(type='bool', default=False), note_events=dict(type='bool', default=False), job_events=dict(type='bool', default=False), pipeline_events=dict(type='bool', default=False), wiki_page_events=dict(type='bool', default=False), hook_validate_certs=dict(type='bool', default=False, aliases=['enable_ssl_verification']), token=dict(type='str', no_log=True)))
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=[['api_username', 'api_token'], ['api_password', 'api_token']], required_together=[['api_username', 'api_password']], required_one_of=[['api_username', 'api_token']], supports_check_mode=True)
    state = module.params['state']
    project_identifier = module.params['project']
    hook_url = module.params['hook_url']
    push_events = module.params['push_events']
    push_events_branch_filter = module.params['push_events_branch_filter']
    issues_events = module.params['issues_events']
    merge_requests_events = module.params['merge_requests_events']
    tag_push_events = module.params['tag_push_events']
    note_events = module.params['note_events']
    job_events = module.params['job_events']
    pipeline_events = module.params['pipeline_events']
    wiki_page_events = module.params['wiki_page_events']
    enable_ssl_verification = module.params['hook_validate_certs']
    hook_token = module.params['token']
    if (not HAS_GITLAB_PACKAGE):
        module.fail_json(msg=missing_required_lib('python-gitlab'), exception=GITLAB_IMP_ERR)
    gitlab_instance = gitlabAuthentication(module)
    gitlab_hook = GitLabHook(module, gitlab_instance)
    project = findProject(gitlab_instance, project_identifier)
    if (project is None):
        module.fail_json(msg=("Failed to create hook: project %s doesn't exists" % project_identifier))
    hook_exists = gitlab_hook.existsHook(project, hook_url)
    if (state == 'absent'):
        if hook_exists:
            gitlab_hook.deleteHook()
            module.exit_json(changed=True, msg=('Successfully deleted hook %s' % hook_url))
        else:
            module.exit_json(changed=False, msg='Hook deleted or does not exists')
    if (state == 'present'):
        if gitlab_hook.createOrUpdateHook(project, hook_url, {
            'push_events': push_events,
            'push_events_branch_filter': push_events_branch_filter,
            'issues_events': issues_events,
            'merge_requests_events': merge_requests_events,
            'tag_push_events': tag_push_events,
            'note_events': note_events,
            'job_events': job_events,
            'pipeline_events': pipeline_events,
            'wiki_page_events': wiki_page_events,
            'enable_ssl_verification': enable_ssl_verification,
            'token': hook_token,
        }):
            module.exit_json(changed=True, msg=('Successfully created or updated the hook %s' % hook_url), hook=gitlab_hook.hookObject._attrs)
        else:
            module.exit_json(changed=False, msg=('No need to update the hook %s' % hook_url), hook=gitlab_hook.hookObject._attrs)