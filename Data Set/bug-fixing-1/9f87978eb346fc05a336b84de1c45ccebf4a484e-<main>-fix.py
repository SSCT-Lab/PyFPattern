

def main():
    argument_spec = dict(certificate=dict(), certificate_arn=dict(aliases=['arn']), certificate_chain=dict(), domain_name=dict(aliases=['domain']), name_tag=dict(aliases=['name']), private_key=dict(no_log=True), state=dict(default='present', choices=['present', 'absent']))
    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True)
    acm = ACMServiceManager(module)
    if (module.params['state'] == 'present'):
        if (not module.params['certificate']):
            module.fail_json(msg="Parameter 'certificate' must be specified if 'state' is specified as 'present'")
        elif module.params['certificate_arn']:
            module.fail_json(msg="Parameter 'certificate_arn' is only valid if parameter 'state' is specified as 'absent'")
        elif (not module.params['name_tag']):
            module.fail_json(msg="Parameter 'name_tag' must be specified if parameter 'state' is specified as 'present'")
        elif (not module.params['private_key']):
            module.fail_json(msg="Parameter 'private_key' must be specified if 'state' is specified as 'present'")
    else:
        absent_args = ['certificate_arn', 'domain_name', 'name_tag']
        if (sum([(module.params[a] is not None) for a in absent_args]) != 1):
            for a in absent_args:
                module.debug(('%s is %s' % (a, module.params[a])))
            module.fail_json(msg="If 'state' is specified as 'absent' then exactly one of 'name_tag', certificate_arn' or 'domain_name' must be specified")
    if module.params['name_tag']:
        tags = dict(Name=module.params['name_tag'])
    else:
        tags = None
    (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
    client = boto3_conn(module, conn_type='client', resource='acm', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    certificates = acm.get_certificates(client=client, module=module, domain_name=module.params['domain_name'], arn=module.params['certificate_arn'], only_tags=tags)
    module.debug(('Found %d corresponding certificates in ACM' % len(certificates)))
    if (module.params['state'] == 'present'):
        if (len(certificates) > 1):
            msg = ('More than one certificate with Name=%s exists in ACM in this region' % module.params['name_tag'])
            module.fail_json(msg=msg, certificates=certificates)
        elif (len(certificates) == 1):
            module.debug('Existing certificate found in ACM')
            old_cert = certificates[0]
            if (('tags' not in old_cert) or ('Name' not in old_cert['tags']) or (old_cert['tags']['Name'] != module.params['name_tag'])):
                module.fail_json(msg='Internal error, unsure which certificate to update', certificate=old_cert)
            if ('certificate' not in old_cert):
                module.fail_json(msg='Internal error, unsure what the existing cert in ACM is', certificate=old_cert)
            same = True
            same &= chain_compare(module, old_cert['certificate'], module.params['certificate'])
            if module.params['certificate_chain']:
                same &= chain_compare(module, old_cert['certificate_chain'], module.params['certificate_chain'])
            else:
                same &= chain_compare(module, old_cert['certificate_chain'], module.params['certificate'])
            if same:
                module.debug('Existing certificate in ACM is the same, doing nothing')
                domain = acm.get_domain_of_cert(client=client, module=module, arn=old_cert['certificate_arn'])
                module.exit_json(certificate=dict(domain_name=domain, arn=old_cert['certificate_arn']), changed=False)
            else:
                module.debug('Existing certificate in ACM is different, overwriting')
                arn = acm.import_certificate(client, module, certificate=module.params['certificate'], private_key=module.params['private_key'], certificate_chain=module.params['certificate_chain'], arn=old_cert['certificate_arn'], tags=tags)
                domain = acm.get_domain_of_cert(client=client, module=module, arn=arn)
                module.exit_json(certificate=dict(domain_name=domain, arn=arn), changed=True)
        else:
            module.debug('No certificate in ACM. Creating new one.')
            arn = acm.import_certificate(client=client, module=module, certificate=module.params['certificate'], private_key=module.params['private_key'], certificate_chain=module.params['certificate_chain'], tags=tags)
            domain = acm.get_domain_of_cert(client=client, module=module, arn=arn)
            module.exit_json(certificate=dict(domain_name=domain, arn=arn), changed=True)
    else:
        for cert in certificates:
            acm.delete_certificate(client, module, cert['certificate_arn'])
        module.exit_json(arns=[cert['certificate_arn'] for cert in certificates], changed=(len(certificates) > 0))
