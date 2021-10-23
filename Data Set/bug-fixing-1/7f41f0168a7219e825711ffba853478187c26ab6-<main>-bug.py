

def main():
    module = AnsibleModule(argument_spec=dict(account_key_src=dict(type='path', aliases=['account_key']), account_key_content=dict(type='str', no_log=True), acme_directory=dict(required=False, default='https://acme-staging.api.letsencrypt.org/directory', type='str'), acme_version=dict(required=False, default=1, choices=[1, 2], type='int'), validate_certs=dict(required=False, default=True, type='bool'), private_key_src=dict(type='path'), private_key_content=dict(type='str', no_log=True), certificate=dict(required=True, type='path'), revoke_reason=dict(required=False, type='int')), required_one_of=(['account_key_src', 'account_key_content', 'private_key_src', 'private_key_content'],), mutually_exclusive=(['account_key_src', 'account_key_content', 'private_key_src', 'private_key_content'],), supports_check_mode=False)
    if (not module.params.get('validate_certs')):
        module.warn(warning=(('Disabling certificate validation for communications with ACME endpoint. ' + 'This should only be done for testing against a local ACME server for ') + 'development purposes, but *never* for production purposes.'))
    try:
        account = ACMEAccount(module)
        certificate_lines = []
        try:
            with open(module.params.get('certificate'), 'rt') as f:
                header_line_count = 0
                for line in f:
                    if line.startswith('-----'):
                        header_line_count += 1
                        if (header_line_count == 2):
                            break
                        continue
                    certificate_lines.append(line.strip())
        except Exception as err:
            raise ModuleFailException(('cannot load certificate file: %s' % to_native(err)), exception=traceback.format_exc())
        certificate = nopad_b64(base64.b64decode(''.join(certificate_lines)))
        payload = {
            'certificate': certificate,
        }
        if (module.params.get('revoke_reason') is not None):
            payload['reason'] = module.params.get('revoke_reason')
        if (module.params.get('acme_version') == 1):
            endpoint = account.directory['revoke-cert']
            payload['resource'] = 'revoke-cert'
        else:
            endpoint = account.directory['revokeCert']
        private_key = module.params.get('private_key_src')
        if (module.params.get('private_key_content') is not None):
            (fd, tmpsrc) = tempfile.mkstemp()
            module.add_cleanup_file(tmpsrc)
            f = os.fdopen(fd, 'wb')
            try:
                f.write(module.params.get('private_key_content').encode('utf-8'))
                private_key = tmpsrc
            except Exception as err:
                try:
                    f.close()
                except Exception as e:
                    pass
                raise ModuleFailException(('failed to create temporary content file: %s' % to_native(err)), exception=traceback.format_exc())
            f.close()
        if private_key:
            (error, private_key_data) = account.parse_account_key(private_key)
            if error:
                raise ModuleFailException(('error while parsing private key: %s' % error))
            jws_header = {
                'alg': private_key_data['alg'],
                'jwk': private_key_data['jwk'],
            }
            (result, info) = account.send_signed_request(endpoint, payload, key=private_key, key_data=private_key_data, jws_header=jws_header)
        else:
            changed = account.init_account([], allow_creation=False, update_contact=False)
            if changed:
                raise AssertionError('Unwanted account change')
            (result, info) = account.send_signed_request(endpoint, payload)
        if (info['status'] != 200):
            if (module.params.get('acme_version') == 1):
                error_type = 'urn:acme:error:malformed'
            else:
                error_type = 'urn:ietf:params:acme:error:malformed'
            if ((result.get('type') == error_type) and (result.get('detail') == 'Certificate already revoked')):
                module.exit_json(changed=False)
            raise ModuleFailException('Error revoking certificate: {0} {1}'.format(info['status'], result))
        module.exit_json(changed=True)
    except ModuleFailException as e:
        e.do_fail(module)
