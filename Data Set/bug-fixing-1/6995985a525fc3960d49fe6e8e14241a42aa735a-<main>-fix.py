

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(zone=dict(required=True), state=dict(default='present', choices=['present', 'absent']), vpc_id=dict(default=None), vpc_region=dict(default=None), comment=dict(default=''), hosted_zone_id=dict()))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module')
    zone_in = module.params.get('zone').lower()
    state = module.params.get('state').lower()
    vpc_id = module.params.get('vpc_id')
    vpc_region = module.params.get('vpc_region')
    if (not zone_in.endswith('.')):
        zone_in += '.'
    private_zone = bool((vpc_id and vpc_region))
    (_, _, aws_connect_kwargs) = get_aws_connection_info(module)
    try:
        conn = Route53Connection(**aws_connect_kwargs)
    except boto.exception.BotoServerError as e:
        module.fail_json(msg=e.error_message)
    zones = find_zones(conn, zone_in, private_zone)
    if (state == 'present'):
        (changed, result) = create(conn, module, matching_zones=zones)
    elif (state == 'absent'):
        (changed, result) = delete(conn, module, matching_zones=zones)
    if isinstance(result, dict):
        module.exit_json(changed=changed, result=result, **result)
    else:
        module.exit_json(changed=changed, result=result)
