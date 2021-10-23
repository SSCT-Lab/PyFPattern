def main():
    argument_spec = dict(cert_url=dict(type='str'), cert_path=dict(type='path'), pkcs12_path=dict(type='path'), pkcs12_password=dict(type='str', no_log=True), pkcs12_alias=dict(type='str'), cert_alias=dict(type='str'), cert_port=dict(type='int', default=443), keystore_path=dict(type='path'), keystore_pass=dict(type='str', required=True, no_log=True), keystore_create=dict(type='bool', default=False), keystore_type=dict(type='str'), executable=dict(type='str', default='keytool'), state=dict(type='str', default='present', choices=['absent', 'present']))
    module = AnsibleModule(argument_spec=argument_spec, required_one_of=[['cert_path', 'cert_url', 'pkcs12_path']], required_together=[['keystore_path', 'keystore_pass']], mutually_exclusive=[['cert_url', 'cert_path', 'pkcs12_path']], supports_check_mode=True)
    url = module.params.get('cert_url')
    path = module.params.get('cert_path')
    port = module.params.get('cert_port')
    pkcs12_path = module.params.get('pkcs12_path')
    pkcs12_pass = module.params.get('pkcs12_password', '')
    pkcs12_alias = module.params.get('pkcs12_alias', '1')
    cert_alias = (module.params.get('cert_alias') or url)
    keystore_path = module.params.get('keystore_path')
    keystore_pass = module.params.get('keystore_pass')
    keystore_create = module.params.get('keystore_create')
    keystore_type = module.params.get('keystore_type')
    executable = module.params.get('executable')
    state = module.params.get('state')
    if (path and (not cert_alias)):
        module.fail_json(changed=False, msg=('Using local path import from %s requires alias argument.' % keystore_path))
    test_keytool(module, executable)
    if (not keystore_create):
        test_keystore(module, keystore_path)
    cert_present = check_cert_present(module, executable, keystore_path, keystore_pass, cert_alias, keystore_type)
    if (state == 'absent'):
        if cert_present:
            delete_cert(module, executable, keystore_path, keystore_pass, cert_alias, keystore_type)
    elif (state == 'present'):
        if (not cert_present):
            if pkcs12_path:
                import_pkcs12_path(module, executable, pkcs12_path, keystore_path, keystore_pass, pkcs12_pass, pkcs12_alias, cert_alias, keystore_type)
            if path:
                import_cert_path(module, executable, path, keystore_path, keystore_pass, cert_alias, keystore_type)
            if url:
                import_cert_url(module, executable, url, port, keystore_path, keystore_pass, cert_alias, keystore_type)
    module.exit_json(changed=False)