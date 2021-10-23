

def main():
    module = AnsibleModule(argument_spec=dict(account_email=dict(required=False), account_api_token=dict(required=False, no_log=True), domain=dict(required=False), record=dict(required=False), record_ids=dict(required=False, type='list'), type=dict(required=False, choices=['A', 'ALIAS', 'CNAME', 'MX', 'SPF', 'URL', 'TXT', 'NS', 'SRV', 'NAPTR', 'PTR', 'AAAA', 'SSHFP', 'HINFO', 'POOL']), ttl=dict(required=False, default=3600, type='int'), value=dict(required=False), priority=dict(required=False, type='int'), state=dict(required=False, choices=['present', 'absent']), solo=dict(required=False, type='bool')), required_together=[['record', 'value']], supports_check_mode=True)
    if (not HAS_DNSIMPLE):
        module.fail_json(msg='dnsimple required for this module')
    if (LooseVersion(dnsimple_version) < LooseVersion('1.0.0')):
        module.fail_json(msg=("Current version of dnsimple Python module [%s] uses 'v1' API which is deprecated. Please upgrade to version 1.0.0 and above to use dnsimple 'v2' API." % dnsimple_version))
    account_email = module.params.get('account_email')
    account_api_token = module.params.get('account_api_token')
    domain = module.params.get('domain')
    record = module.params.get('record')
    record_ids = module.params.get('record_ids')
    record_type = module.params.get('type')
    ttl = module.params.get('ttl')
    value = module.params.get('value')
    priority = module.params.get('priority')
    state = module.params.get('state')
    is_solo = module.params.get('solo')
    if (account_email and account_api_token):
        client = DNSimple(email=account_email, api_token=account_api_token)
    elif (os.environ.get('DNSIMPLE_EMAIL') and os.environ.get('DNSIMPLE_API_TOKEN')):
        client = DNSimple(email=os.environ.get('DNSIMPLE_EMAIL'), api_token=os.environ.get('DNSIMPLE_API_TOKEN'))
    else:
        client = DNSimple()
    try:
        if (not domain):
            domains = client.domains()
            module.exit_json(changed=False, result=[d['domain'] for d in domains])
        if (domain and (record is None) and (not record_ids)):
            domains = [d['domain'] for d in client.domains()]
            if domain.isdigit():
                dr = next((d for d in domains if (d['id'] == int(domain))), None)
            else:
                dr = next((d for d in domains if (d['name'] == domain)), None)
            if (state == 'present'):
                if dr:
                    module.exit_json(changed=False, result=dr)
                elif module.check_mode:
                    module.exit_json(changed=True)
                else:
                    module.exit_json(changed=True, result=client.add_domain(domain)['domain'])
            elif (state == 'absent'):
                if dr:
                    if (not module.check_mode):
                        client.delete(domain)
                    module.exit_json(changed=True)
                else:
                    module.exit_json(changed=False)
            else:
                module.fail_json(msg=("'%s' is an unknown value for the state argument" % state))
        if (domain and (record is not None)):
            records = [r['record'] for r in client.records(str(domain))]
            if (not record_type):
                module.fail_json(msg='Missing the record type')
            if (not value):
                module.fail_json(msg='Missing the record value')
            rr = next((r for r in records if ((r['name'] == record) and (r['record_type'] == record_type) and (r['content'] == value))), None)
            if (state == 'present'):
                changed = False
                if is_solo:
                    same_type = [r['id'] for r in records if ((r['name'] == record) and (r['record_type'] == record_type))]
                    if rr:
                        same_type = [rid for rid in same_type if (rid != rr['id'])]
                    if same_type:
                        if (not module.check_mode):
                            for rid in same_type:
                                client.delete_record(str(domain), rid)
                        changed = True
                if rr:
                    if ((rr['ttl'] != ttl) or (rr['prio'] != priority)):
                        data = {
                            
                        }
                        if ttl:
                            data['ttl'] = ttl
                        if priority:
                            data['prio'] = priority
                        if module.check_mode:
                            module.exit_json(changed=True)
                        else:
                            module.exit_json(changed=True, result=client.update_record(str(domain), str(rr['id']), data)['record'])
                    else:
                        module.exit_json(changed=changed, result=rr)
                else:
                    data = {
                        'name': record,
                        'record_type': record_type,
                        'content': value,
                    }
                    if ttl:
                        data['ttl'] = ttl
                    if priority:
                        data['prio'] = priority
                    if module.check_mode:
                        module.exit_json(changed=True)
                    else:
                        module.exit_json(changed=True, result=client.add_record(str(domain), data)['record'])
            elif (state == 'absent'):
                if rr:
                    if (not module.check_mode):
                        client.delete_record(str(domain), rr['id'])
                    module.exit_json(changed=True)
                else:
                    module.exit_json(changed=False)
            else:
                module.fail_json(msg=("'%s' is an unknown value for the state argument" % state))
        if (domain and record_ids):
            current_records = [str(r['record']['id']) for r in client.records(str(domain))]
            wanted_records = [str(r) for r in record_ids]
            if (state == 'present'):
                difference = list((set(wanted_records) - set(current_records)))
                if difference:
                    module.fail_json(msg=('Missing the following records: %s' % difference))
                else:
                    module.exit_json(changed=False)
            elif (state == 'absent'):
                difference = list((set(wanted_records) & set(current_records)))
                if difference:
                    if (not module.check_mode):
                        for rid in difference:
                            client.delete_record(str(domain), rid)
                    module.exit_json(changed=True)
                else:
                    module.exit_json(changed=False)
            else:
                module.fail_json(msg=("'%s' is an unknown value for the state argument" % state))
    except DNSimpleException as e:
        module.fail_json(msg=('Unable to contact DNSimple: %s' % e.message))
    module.fail_json(msg='Unknown what you wanted me to do')
