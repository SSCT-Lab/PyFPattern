def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state=dict(choices=['enable', 'disable']), table_name=dict(required=True), attribute_name=dict(required=True)))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 required for this module')
    elif (distutils.version.StrictVersion(botocore.__version__) < distutils.version.StrictVersion('1.5.24')):
        module.fail_json(msg='Found botocore in version {0}, but >= {1} is required for TTL support'.format(botocore.__version__, '1.5.24'))
    try:
        (region, ec2_url, aws_connect_kwargs) = ansible.module_utils.ec2.get_aws_connection_info(module, boto3=True)
        dbclient = ansible.module_utils.ec2.boto3_conn(module, conn_type='client', resource='dynamodb', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except botocore.exceptions.NoCredentialsError as e:
        module.fail_json(msg=str(e))
    result = {
        'changed': False,
    }
    state = module.params['state']
    try:
        current_state = get_current_ttl_state(dbclient, module.params['table_name'])
        if does_state_need_changing(module.params['attribute_name'], module.params['state'], current_state):
            new_state = set_ttl_state(dbclient, module.params['table_name'], module.params['state'], module.params['attribute_name'])
            result['current_status'] = new_state
            result['changed'] = True
        else:
            result['current_status'] = current_state
    except (botocore.exceptions.ClientError, botocore.exceptions.ParamValidationError) as e:
        module.fail_json(msg=e.message, **camel_dict_to_snake_dict(e.response))
    except ValueError as e:
        module.fail_json(msg=str(e))
    module.exit_json(**result)