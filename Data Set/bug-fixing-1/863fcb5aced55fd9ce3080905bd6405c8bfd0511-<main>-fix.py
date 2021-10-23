

def main():
    argument_spec = url_argument_spec()
    argument_spec.update(group=dict(default='jenkins'), jenkins_home=dict(default='/var/lib/jenkins'), mode=dict(default='0644', type='raw'), name=dict(required=True), owner=dict(default='jenkins'), params=dict(type='dict'), state=dict(choices=['present', 'absent', 'pinned', 'unpinned', 'enabled', 'disabled', 'latest'], default='present'), timeout=dict(default=30, type='int'), updates_expiration=dict(default=86400, type='int'), updates_url=dict(default='https://updates.jenkins-ci.org'), url=dict(default='http://localhost:8080'), url_password=dict(no_log=True), version=dict(), with_dependencies=dict(default=True, type='bool'))
    module = AnsibleModule(argument_spec=argument_spec, add_file_common_args=True, supports_check_mode=True)
    if (('params' in module.params) and isinstance(module.params['params'], dict)):
        if ('url_password' in module.params['params']):
            module.fail_json(msg='Do not specify url_password in params as it may get logged')
        module.params.update(module.params['params'])
        module.params.pop('params', None)
    module.params['force_basic_auth'] = True
    try:
        module.params['timeout'] = float(module.params['timeout'])
    except ValueError:
        e = get_exception()
        module.fail_json(msg=('Cannot convert %s to float.' % module.params['timeout']), details=to_native(e))
    if (module.params['state'] == 'latest'):
        module.params['state'] = 'present'
        module.params['version'] = 'latest'
    name = module.params['name']
    state = module.params['state']
    changed = False
    jp = JenkinsPlugin(module)
    if (state == 'present'):
        changed = jp.install()
    elif (state == 'absent'):
        changed = jp.uninstall()
    elif (state == 'pinned'):
        changed = jp.pin()
    elif (state == 'unpinned'):
        changed = jp.unpin()
    elif (state == 'enabled'):
        changed = jp.enable()
    elif (state == 'disabled'):
        changed = jp.disable()
    module.exit_json(changed=changed, plugin=name, state=state)
