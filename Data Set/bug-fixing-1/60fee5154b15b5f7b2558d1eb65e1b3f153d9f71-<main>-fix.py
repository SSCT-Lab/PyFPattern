

def main():
    module = AnsibleModule(argument_spec=dict(account_key_src=dict(type='path', aliases=['account_key']), account_key_content=dict(type='str', no_log=True), account_email=dict(required=False, default=None, type='str'), acme_directory=dict(required=False, default='https://acme-staging.api.letsencrypt.org/directory', type='str'), acme_version=dict(required=False, default=1, choices=[1, 2], type='int'), agreement=dict(required=False, type='str'), terms_agreed=dict(required=False, default=False, type='bool'), challenge=dict(required=False, default='http-01', choices=['http-01', 'dns-01', 'tls-sni-02'], type='str'), csr=dict(required=True, aliases=['src'], type='path'), data=dict(required=False, default=None, type='dict'), dest=dict(aliases=['cert'], type='path'), fullchain_dest=dict(aliases=['fullchain'], type='path'), chain_dest=dict(required=False, default=None, aliases=['chain'], type='path'), remaining_days=dict(required=False, default=10, type='int'), validate_certs=dict(required=False, default=True, type='bool'), deactivate_authzs=dict(required=False, default=False, type='bool'), force=dict(required=False, default=False, type='bool')), required_one_of=(['account_key_src', 'account_key_content'], ['dest', 'fullchain_dest']), mutually_exclusive=(['account_key_src', 'account_key_content'],), supports_check_mode=True)
    module.run_command_environ_update = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C', LC_CTYPE='C')
    locale.setlocale(locale.LC_ALL, 'C')
    if (not module.params.get('validate_certs')):
        module.warn(warning=(('Disabling certificate validation for communications with ACME endpoint. ' + 'This should only be done for testing against a local ACME server for ') + 'development purposes, but *never* for production purposes.'))
    try:
        if module.params.get('dest'):
            cert_days = get_cert_days(module, module.params['dest'])
        else:
            cert_days = get_cert_days(module, module.params['fullchain_dest'])
        if (module.params['force'] or (cert_days < module.params['remaining_days'])):
            if module.check_mode:
                module.exit_json(changed=True, authorizations={
                    
                }, challenge_data={
                    
                }, cert_days=cert_days)
            else:
                client = ACMEClient(module)
                client.cert_days = cert_days
                if client.is_first_step():
                    client.start_challenges()
                else:
                    try:
                        client.finish_challenges()
                        client.get_certificate()
                    finally:
                        if module.params['deactivate_authzs']:
                            client.deactivate_authzs()
                (data, data_dns) = client.get_challenges_data()
                module.exit_json(changed=client.changed, authorizations=client.authorizations, finalize_uri=client.finalize_uri, order_uri=client.order_uri, account_uri=client.account.uri, challenge_data=data, challenge_data_dns=data_dns, cert_days=client.cert_days)
        else:
            module.exit_json(changed=False, cert_days=cert_days)
    except ModuleFailException as e:
        e.do_fail(module)
