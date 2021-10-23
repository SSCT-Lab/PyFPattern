

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state=dict(aliases=['command'], choices=['present', 'absent', 'get', 'create', 'delete'], required=True), zone=dict(required=True), hosted_zone_id=dict(required=False, default=None), record=dict(required=True), ttl=dict(required=False, type='int', default=3600), type=dict(choices=['A', 'CNAME', 'MX', 'AAAA', 'TXT', 'PTR', 'SRV', 'SPF', 'NS', 'SOA'], required=True), alias=dict(required=False, type='bool'), alias_hosted_zone_id=dict(required=False), alias_evaluate_target_health=dict(required=False, type='bool', default=False), value=dict(required=False, type='list', default=[]), overwrite=dict(required=False, type='bool'), retry_interval=dict(required=False, default=500), private_zone=dict(required=False, type='bool', default=False), identifier=dict(required=False, default=None), weight=dict(required=False, type='int'), region=dict(required=False), health_check=dict(required=False), failover=dict(required=False, choices=['PRIMARY', 'SECONDARY']), vpc_id=dict(required=False), wait=dict(required=False, type='bool', default=False), wait_timeout=dict(required=False, type='int', default=300)))
    required_if = [('state', 'present', ['value']), ('state', 'create', ['value'])]
    required_if.extend([('state', 'absent', ['value']), ('state', 'delete', ['value'])])
    required_together = [['alias', 'alias_hosted_zone_id']]
    mutually_exclusive = [('failover', 'region', 'weight')]
    module = AnsibleModule(argument_spec=argument_spec, required_together=required_together, required_if=required_if, mutually_exclusive=mutually_exclusive)
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module')
    if (distutils.version.StrictVersion(boto.__version__) < distutils.version.StrictVersion(MINIMUM_BOTO_VERSION)):
        module.fail_json(msg=('Found boto in version %s, but >= %s is required' % (boto.__version__, MINIMUM_BOTO_VERSION)))
    if (module.params['state'] in ('present', 'create')):
        command_in = 'create'
    elif (module.params['state'] in ('absent', 'delete')):
        command_in = 'delete'
    elif (module.params['state'] == 'get'):
        command_in = 'get'
    zone_in = module.params.get('zone').lower()
    hosted_zone_id_in = module.params.get('hosted_zone_id')
    ttl_in = module.params.get('ttl')
    record_in = module.params.get('record').lower()
    type_in = module.params.get('type')
    value_in = module.params.get('value')
    alias_in = module.params.get('alias')
    alias_hosted_zone_id_in = module.params.get('alias_hosted_zone_id')
    alias_evaluate_target_health_in = module.params.get('alias_evaluate_target_health')
    retry_interval_in = module.params.get('retry_interval')
    if (module.params['vpc_id'] is not None):
        private_zone_in = True
    else:
        private_zone_in = module.params.get('private_zone')
    identifier_in = module.params.get('identifier')
    weight_in = module.params.get('weight')
    region_in = module.params.get('region')
    health_check_in = module.params.get('health_check')
    failover_in = module.params.get('failover')
    vpc_id_in = module.params.get('vpc_id')
    wait_in = module.params.get('wait')
    wait_timeout_in = module.params.get('wait_timeout')
    (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module)
    if (zone_in[(- 1):] != '.'):
        zone_in += '.'
    if (record_in[(- 1):] != '.'):
        record_in += '.'
    if ((command_in == 'create') or (command_in == 'delete')):
        if (alias_in and (len(value_in) != 1)):
            module.fail_json(msg="parameter 'value' must contain a single dns name for alias records")
        if (((weight_in is not None) or (region_in is not None) or (failover_in is not None)) and (identifier_in is None)):
            module.fail_json(msg='If you specify failover, region or weight you must also specify identifier')
        if (((weight_in is None) and (region_in is None) and (failover_in is None)) and (identifier_in is not None)):
            module.fail_json(msg='You have specified identifier which makes sense only if you specify one of: weight, region or failover.')
    try:
        conn = Route53Connection(**aws_connect_kwargs)
    except boto.exception.BotoServerError as e:
        module.fail_json(msg=e.error_message)
    zone = get_zone_by_name(conn, module, zone_in, private_zone_in, hosted_zone_id_in, vpc_id_in)
    if (zone is None):
        errmsg = ('Zone %s does not exist in Route53' % zone_in)
        module.fail_json(msg=errmsg)
    record = {
        
    }
    found_record = False
    wanted_rset = Record(name=record_in, type=type_in, ttl=ttl_in, identifier=identifier_in, weight=weight_in, region=region_in, health_check=health_check_in, failover=failover_in)
    for v in value_in:
        if alias_in:
            wanted_rset.set_alias(alias_hosted_zone_id_in, v, alias_evaluate_target_health_in)
        else:
            wanted_rset.add_value(v)
    sets = invoke_with_throttling_retries(conn.get_all_rrsets, zone.id, name=record_in, type=type_in, identifier=identifier_in)
    sets_iter = iter(sets)
    while True:
        try:
            rset = invoke_with_throttling_retries(next, sets_iter)
        except StopIteration:
            break
        decoded_name = rset.name.replace('\\052', '*')
        decoded_name = decoded_name.replace('\\100', '@')
        rset.name = decoded_name
        if (identifier_in is not None):
            identifier_in = str(identifier_in)
        if ((rset.type == type_in) and (decoded_name.lower() == record_in.lower()) and (rset.identifier == identifier_in)):
            found_record = True
            record['zone'] = zone_in
            record['type'] = rset.type
            record['record'] = decoded_name
            record['ttl'] = rset.ttl
            record['value'] = ','.join(sorted(rset.resource_records))
            record['values'] = sorted(rset.resource_records)
            if hosted_zone_id_in:
                record['hosted_zone_id'] = hosted_zone_id_in
            record['identifier'] = rset.identifier
            record['weight'] = rset.weight
            record['region'] = rset.region
            record['failover'] = rset.failover
            record['health_check'] = rset.health_check
            if hosted_zone_id_in:
                record['hosted_zone_id'] = hosted_zone_id_in
            if rset.alias_dns_name:
                record['alias'] = True
                record['value'] = rset.alias_dns_name
                record['values'] = [rset.alias_dns_name]
                record['alias_hosted_zone_id'] = rset.alias_hosted_zone_id
                record['alias_evaluate_target_health'] = rset.alias_evaluate_target_health
            else:
                record['alias'] = False
                record['value'] = ','.join(sorted(rset.resource_records))
                record['values'] = sorted(rset.resource_records)
            if ((command_in == 'create') and (rset.to_xml() == wanted_rset.to_xml())):
                module.exit_json(changed=False)
        break
    if (command_in == 'get'):
        if (type_in == 'NS'):
            ns = record.get('values', [])
        else:
            z = invoke_with_throttling_retries(conn.get_zone, zone_in)
            ns = invoke_with_throttling_retries(z.get_nameservers)
        module.exit_json(changed=False, set=record, nameservers=ns)
    if ((command_in == 'delete') and (not found_record)):
        module.exit_json(changed=False)
    changes = ResourceRecordSets(conn, zone.id)
    if ((command_in == 'create') or (command_in == 'delete')):
        if ((command_in == 'create') and found_record):
            if (not module.params['overwrite']):
                module.fail_json(msg="Record already exists with different value. Set 'overwrite' to replace it")
            command = 'UPSERT'
        else:
            command = command_in.upper()
        changes.add_change_record(command, wanted_rset)
    try:
        result = invoke_with_throttling_retries(commit, changes, retry_interval_in, wait_in, wait_timeout_in)
    except boto.route53.exception.DNSServerError as e:
        txt = e.body.split('<Message>')[1]
        txt = txt.split('</Message>')[0]
        if ('but it already exists' in txt):
            module.exit_json(changed=False)
        else:
            module.fail_json(msg=txt)
    except TimeoutError:
        module.fail_json(msg='Timeout waiting for changes to replicate')
    module.exit_json(changed=True)
