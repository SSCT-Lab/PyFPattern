def main():
    module = AnsibleModule(argument_spec=dict(account_key=dict(required=True, type='path'), account_email=dict(required=False, default=None, type='str'), acme_directory=dict(required=False, default='https://acme-staging.api.letsencrypt.org/directory', type='str'), agreement=dict(required=False, default='https://letsencrypt.org/documents/LE-SA-v1.1.1-August-1-2016.pdf', type='str'), challenge=dict(required=False, default='http-01', choices=['http-01', 'dns-01', 'tls-sni-02'], type='str'), csr=dict(required=True, aliases=['src'], type='path'), data=dict(required=False, no_log=True, default=None, type='dict'), dest=dict(required=True, aliases=['cert'], type='path'), remaining_days=dict(required=False, default=10, type='int')), supports_check_mode=True)
    module.run_command_environ_update = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C', LC_CTYPE='C')
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