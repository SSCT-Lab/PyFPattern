def main():
    'The main function.'
    module = AnsibleModule(argument_spec=dict(host=dict(type='str', default='localhost'), port=dict(type='int', default=44134), name=dict(type='str', default=''), chart=dict(type='dict'), state=dict(choices=['absent', 'purged', 'present'], default='present'), values=dict(type='dict'), namespace=dict(type='str', default='default'), disable_hooks=dict(type='bool', default=False)), supports_check_mode=True)
    if HELM_IMPORT_ERR:
        module.fail_json(msg=missing_required_lib('pyhelm'), exception=HELM_IMPORT_ERR)
    host = module.params['host']
    port = module.params['port']
    state = module.params['state']
    tserver = tiller.Tiller(host, port)
    if (state == 'present'):
        rst = install(module, tserver)
    if (state in 'absent'):
        rst = delete(module, tserver)
    if (state in 'purged'):
        rst = delete(module, tserver, True)
    module.exit_json(**rst)