def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state={
        'required': True,
        'choices': ['enabled', 'disabled'],
    }, name={
        'required': True,
        'type': 'str',
    }, s3_bucket_name={
        'required': False,
        'type': 'str',
    }, s3_key_prefix={
        'default': '',
        'required': False,
        'type': 'str',
    }, include_global_events={
        'default': True,
        'required': False,
        'type': 'bool',
    }))
    required_together = ['state', 's3_bucket_name']
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_together=required_together)
    if (not HAS_BOTO):
        module.fail_json(msg='boto is required.')
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module)
    if (not region):
        module.fail_json(msg='Region must be specified as a parameter, in EC2_REGION or AWS_REGION environment variables or in boto configuration file')
    ct_name = module.params['name']
    s3_bucket_name = module.params['s3_bucket_name']
    s3_key_prefix = module.params['s3_key_prefix'].rstrip('/')
    include_global_events = module.params['include_global_events']
    cf_man = CloudTrailManager(module, region=region, **aws_connect_params)
    results = {
        'changed': False,
    }
    if (module.params['state'] == 'enabled'):
        results['exists'] = cf_man.exists(name=ct_name)
        if results['exists']:
            results['view'] = cf_man.view(ct_name)
            if ((results['view']['S3BucketName'] != s3_bucket_name) or (results['view'].get('S3KeyPrefix', '') != s3_key_prefix) or (results['view']['IncludeGlobalServiceEvents'] != include_global_events)):
                if (not module.check_mode):
                    results['update'] = cf_man.update(name=ct_name, s3_bucket_name=s3_bucket_name, s3_key_prefix=s3_key_prefix, include_global_service_events=include_global_events)
                results['changed'] = True
        else:
            if (not module.check_mode):
                results['enable'] = cf_man.enable(name=ct_name, s3_bucket_name=s3_bucket_name, s3_key_prefix=s3_key_prefix, include_global_service_events=include_global_events)
            results['changed'] = True
        results['view_status'] = cf_man.view_status(ct_name)
        results['was_logging_enabled'] = results['view_status'].get('IsLogging', False)
        if (not results['was_logging_enabled']):
            if (not module.check_mode):
                cf_man.enable_logging(ct_name)
                results['logging_enabled'] = True
            results['changed'] = True
    elif (module.params['state'] == 'disabled'):
        results['exists'] = cf_man.exists(name=ct_name)
        if results['exists']:
            if (not module.check_mode):
                cf_man.delete(ct_name)
            results['changed'] = True
    module.exit_json(**results)