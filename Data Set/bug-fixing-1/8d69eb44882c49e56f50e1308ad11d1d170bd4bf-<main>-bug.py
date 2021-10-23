

def main():
    module = AnsibleModule(argument_spec=dict(account_key_src=dict(type='path', aliases=['account_key']), account_key_content=dict(type='str'), account_email=dict(required=False, default=None, type='str'), acme_directory=dict(required=False, default='https://acme-staging.api.letsencrypt.org/directory', type='str'), agreement=dict(required=False, type='str'), challenge=dict(required=False, default='http-01', choices=['http-01', 'dns-01', 'tls-sni-02'], type='str'), csr=dict(required=True, aliases=['src'], type='path'), data=dict(required=False, no_log=True, default=None, type='dict'), fullchain=dict(required=False, default=True, type='bool'), dest=dict(required=True, aliases=['cert'], type='path'), remaining_days=dict(required=False, default=10, type='int')), required_one_of=(['account_key_src', 'account_key_content'],), mutually_exclusive=(['account_key_src', 'account_key_content'],), supports_check_mode=True)
    module.run_command_environ_update = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C', LC_CTYPE='C')
    locale.setlocale(locale.LC_ALL, 'C')
    cert_days = get_cert_days(module, module.params['dest'])
    if (cert_days < module.params['remaining_days']):
        if module.check_mode:
            module.exit_json(changed=True, authorizations={
                
            }, challenge_data={
                
            }, cert_days=cert_days)
        else:
            client = ACMEClient(module)
            client.cert_days = cert_days
            data = client.do_challenges()
            client.get_certificate()
            module.exit_json(changed=client.changed, authorizations=client.authorizations, challenge_data=data, cert_days=client.cert_days)
    else:
        module.exit_json(changed=False, cert_days=cert_days)
