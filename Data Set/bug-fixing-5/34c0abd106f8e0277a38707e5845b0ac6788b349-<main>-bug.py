def main():
    module = AnsibleModule(argument_spec=dict(state=dict(default='present', choices=['present', 'absent'], type='str'), digest=dict(default='sha256', type='str'), privatekey_path=dict(require=True, type='path'), version=dict(default='3', type='int'), force=dict(default=False, type='bool'), subjectAltName=dict(aliases=['subjectAltName'], type='str'), path=dict(required=True, type='path'), countryName=dict(aliases=['C'], type='str'), stateOrProvinceName=dict(aliases=['ST'], type='str'), localityName=dict(aliases=['L'], type='str'), organizationName=dict(aliases=['O'], type='str'), organizationalUnitName=dict(aliases=['OU'], type='str'), commonName=dict(aliases=['CN'], type='str'), emailAddress=dict(aliases=['E'], type='str')), add_file_common_args=True, supports_check_mode=True, required_one_of=[['commonName', 'subjectAltName']])
    path = module.params['path']
    base_dir = os.path.dirname(module.params['path'])
    if (not os.path.isdir(base_dir)):
        module.fail_json(name=path, msg=('The directory %s does not exist' % path))
    csr = CertificateSigningRequest(module)
    if (module.params['state'] == 'present'):
        if module.check_mode:
            result = csr.dump()
            result['changed'] = (module.params['force'] or (not os.path.exists(path)))
            module.exit_json(**result)
        try:
            csr.generate(module)
        except CertificateSigningRequestError as exc:
            module.fail_json(msg=to_native(exc))
    else:
        if module.check_mode:
            result = csr.dump()
            result['changed'] = os.path.exists(path)
            module.exit_json(**result)
        try:
            csr.remove()
        except CertificateSigningRequestError as exc:
            module.fail_json(msg=to_native(exc))
    result = csr.dump()
    module.exit_json(**result)