

def main():
    module = AnsibleModule(argument_spec=dict(name=dict(type='str', required=True), flatpakrepo_url=dict(type='str'), method=dict(type='str', default='system', choices=['user', 'system']), state=dict(type='str', default='present', choices=['absent', 'present']), executable=dict(type='str', default='flatpak')), supports_check_mode=True)
    name = module.params['name']
    flatpakrepo_url = module.params['flatpakrepo_url']
    method = module.params['method']
    state = module.params['state']
    executable = module.params['executable']
    binary = module.get_bin_path(executable, None)
    if (flatpakrepo_url is None):
        flatpakrepo_url = ''
    global result
    result = dict(changed=False)
    if (not binary):
        module.fail_json(msg=("Executable '%s' was not found on the system." % executable), **result)
    remote_already_exists = remote_exists(module, binary, bytes(name, 'utf-8'), method)
    if ((state == 'present') and (not remote_already_exists)):
        add_remote(module, binary, name, flatpakrepo_url, method)
    elif ((state == 'absent') and remote_already_exists):
        remove_remote(module, binary, name, method)
    module.exit_json(**result)
