

def main():
    argument_spec = dict(cert_url=dict(type='str'), cert_path=dict(type='str'), cert_alias=dict(type='str'), cert_port=dict(default='443', type='int'), keystore_path=dict(type='str'), keystore_pass=dict(required=True, type='str'), keystore_create=dict(default=False, type='bool'), executable=dict(default='keytool', type='str'), state=dict(default='present', choices=['present', 'absent']))
    module = AnsibleModule(argument_spec=argument_spec, required_one_of=[['cert_path', 'cert_url']], required_together=[['keystore_path', 'keystore_pass']], mutually_exclusive=[['cert_url', 'cert_path']], supports_check_mode=True)
    url = module.params.get('cert_url')
    path = module.params.get('cert_path')
    port = module.params.get('cert_port')
    cert_alias = (module.params.get('cert_alias') or url)
    keystore_path = module.params.get('keystore_path')
    keystore_pass = module.params.get('keystore_pass')
    keystore_create = module.params.get('keystore_create')
    executable = module.params.get('executable')
    state = module.params.get('state')
    if (path and (not cert_alias)):
        module.fail_json(changed=False, msg=('Using local path import from %s requires alias argument.' % keystore_path))
    test_keytool(module, executable)
    if (not keystore_create):
        test_keystore(module, keystore_path)
    cert_present = check_cert_present(module, executable, keystore_path, keystore_pass, cert_alias)
    if (state == 'absent'):
        if cert_present:
            delete_cert(module, executable, keystore_path, keystore_pass, cert_alias)
    elif (state == 'present'):
        if (not cert_present):
            if path:
                import_cert_path(module, executable, path, keystore_path, keystore_pass, cert_alias)
            if url:
                import_cert_url(module, executable, url, port, keystore_path, keystore_pass, cert_alias)
    module.exit_json(changed=False)
