

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(name=dict(required=True), version=dict(required=False), description=dict(required=False, default=''), objects=dict(required=False, type='list', default=[]), parameters=dict(required=False, type='list', default=[]), timeout=dict(required=False, type='int', default=300), state=dict(default='present', choices=['present', 'absent', 'active', 'inactive']), tags=dict(required=False, type='dict', default={
        
    }), values=dict(required=False, type='list', default=[])))
    module = AnsibleModule(argument_spec, supports_check_mode=False)
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 is required for the datapipeline module!')
    try:
        (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
        if (not region):
            module.fail_json(msg='Region must be specified as a parameter, in EC2_REGION or AWS_REGION environment variables or in boto configuration file')
        client = boto3_conn(module, conn_type='client', resource='datapipeline', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except ClientError as e:
        module.fail_json(msg=("Can't authorize connection - " + str(e)))
    state = module.params.get('state')
    if (state == 'present'):
        (changed, result) = create_pipeline(client, module)
    elif (state == 'absent'):
        (changed, result) = delete_pipeline(client, module)
    elif (state == 'active'):
        (changed, result) = activate_pipeline(client, module)
    elif (state == 'inactive'):
        (changed, result) = deactivate_pipeline(client, module)
    module.exit_json(result=result, changed=changed)
