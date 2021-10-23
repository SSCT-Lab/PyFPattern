def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(access_logs_enabled=dict(type='bool'), access_logs_s3_bucket=dict(type='str'), access_logs_s3_prefix=dict(type='str'), deletion_protection=dict(type='bool'), http2=dict(type='bool'), idle_timeout=dict(type='int'), listeners=dict(type='list', elements='dict', options=dict(Protocol=dict(type='str', required=True), Port=dict(type='int', required=True), SslPolicy=dict(type='str'), Certificates=dict(type='list'), DefaultActions=dict(type='list', required=True), Rules=dict(type='list'))), name=dict(required=True, type='str'), purge_listeners=dict(default=True, type='bool'), purge_tags=dict(default=True, type='bool'), subnets=dict(type='list'), security_groups=dict(type='list'), scheme=dict(default='internet-facing', choices=['internet-facing', 'internal']), state=dict(choices=['present', 'absent'], default='present'), tags=dict(type='dict'), wait_timeout=dict(type='int'), wait=dict(default=False, type='bool'), purge_rules=dict(default=True, type='bool')))
    module = AnsibleAWSModule(argument_spec=argument_spec, required_if=[('state', 'present', ['subnets', 'security_groups'])], required_together=[['access_logs_enabled', 'access_logs_s3_bucket', 'access_logs_s3_prefix']])
    listeners = module.params.get('listeners')
    if (listeners is not None):
        for listener in listeners:
            for key in listener.keys():
                if ((key == 'Protocol') and (listener[key] == 'HTTPS')):
                    if (listener.get('SslPolicy') is None):
                        module.fail_json(msg="'SslPolicy' is a required listener dict key when Protocol = HTTPS")
                    if (listener.get('Certificates') is None):
                        module.fail_json(msg="'Certificates' is a required listener dict key when Protocol = HTTPS")
    connection = module.client('elbv2')
    connection_ec2 = module.client('ec2')
    state = module.params.get('state')
    elb = ApplicationLoadBalancer(connection, connection_ec2, module)
    if (state == 'present'):
        create_or_update_elb(elb)
    else:
        delete_elb(elb)