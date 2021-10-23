

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state=dict(default='present', choices=['present', 'absent', 'enabled', 'disabled']), name=dict(default='default'), enable_logging=dict(default=True, type='bool'), s3_bucket_name=dict(), s3_key_prefix=dict(), sns_topic_name=dict(), is_multi_region_trail=dict(default=False, type='bool'), enable_log_file_validation=dict(type='bool', aliases=['log_file_validation_enabled']), include_global_events=dict(default=True, type='bool', aliases=['include_global_service_events']), cloudwatch_logs_role_arn=dict(), cloudwatch_logs_log_group_arn=dict(), kms_key_id=dict(), tags=dict(default={
        
    }, type='dict')))
    required_if = [('state', 'present', ['s3_bucket_name']), ('state', 'enabled', ['s3_bucket_name'])]
    required_together = [('cloudwatch_logs_role_arn', 'cloudwatch_logs_log_group_arn')]
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_together=required_together, required_if=required_if)
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 is required for this module')
    if (module.params['state'] in ('present', 'enabled')):
        state = 'present'
    elif (module.params['state'] in ('absent', 'disabled')):
        state = 'absent'
    tags = module.params['tags']
    enable_logging = module.params['enable_logging']
    ct_params = dict(Name=module.params['name'], S3BucketName=module.params['s3_bucket_name'], IncludeGlobalServiceEvents=module.params['include_global_events'], IsMultiRegionTrail=module.params['is_multi_region_trail'])
    if module.params['s3_key_prefix']:
        ct_params['S3KeyPrefix'] = module.params['s3_key_prefix'].rstrip('/')
    if module.params['sns_topic_name']:
        ct_params['SnsTopicName'] = module.params['sns_topic_name']
    if module.params['cloudwatch_logs_role_arn']:
        ct_params['CloudWatchLogsRoleArn'] = module.params['cloudwatch_logs_role_arn']
    if module.params['cloudwatch_logs_log_group_arn']:
        ct_params['CloudWatchLogsLogGroupArn'] = module.params['cloudwatch_logs_log_group_arn']
    if (module.params['enable_log_file_validation'] is not None):
        ct_params['EnableLogFileValidation'] = module.params['enable_log_file_validation']
    if module.params['kms_key_id']:
        ct_params['KmsKeyId'] = module.params['kms_key_id']
    try:
        (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
        client = boto3_conn(module, conn_type='client', resource='cloudtrail', region=region, endpoint=ec2_url, **aws_connect_params)
    except ClientError as err:
        module.fail_json(msg=err.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(err.response))
    results = dict(changed=False, exists=False)
    trail = get_trail_facts(module, client, ct_params['Name'])
    if (trail is not None):
        results['exists'] = True
    if ((state == 'absent') and results['exists']):
        results['changed'] = True
        results['exists'] = False
        results['trail'] = dict()
        if (not module.check_mode):
            delete_trail(module, client, trail['TrailARN'])
    elif ((state == 'present') and results['exists']):
        do_update = False
        for key in ct_params:
            tkey = str(key)
            if (key == 'EnableLogFileValidation'):
                tkey = 'LogFileValidationEnabled'
            if (ct_params.get(key) == ''):
                val = None
            else:
                val = ct_params.get(key)
            if (val != trail.get(tkey)):
                do_update = True
                results['changed'] = True
                if module.check_mode:
                    trail.update({
                        tkey: ct_params.get(key),
                    })
        if ((not module.check_mode) and do_update):
            update_trail(module, client, ct_params)
            trail = get_trail_facts(module, client, ct_params['Name'])
        if (enable_logging and (not trail['IsLogging'])):
            results['changed'] = True
            trail['IsLogging'] = True
            if (not module.check_mode):
                set_logging(module, client, name=ct_params['Name'], action='start')
        if ((not enable_logging) and trail['IsLogging']):
            results['changed'] = True
            trail['IsLogging'] = False
            if (not module.check_mode):
                set_logging(module, client, name=ct_params['Name'], action='stop')
        tag_dry_run = False
        if module.check_mode:
            tag_dry_run = True
        tags_changed = tag_trail(module, client, tags=tags, trail_arn=trail['TrailARN'], curr_tags=trail['tags'], dry_run=tag_dry_run)
        if tags_changed:
            results['changed'] = True
            trail['tags'] = tags
        results['trail'] = camel_dict_to_snake_dict(trail)
    elif ((state == 'present') and (not results['exists'])):
        results['changed'] = True
        if (not module.check_mode):
            created_trail = create_trail(module, client, ct_params)
            tag_trail(module, client, tags=tags, trail_arn=created_trail['TrailARN'])
            try:
                status_resp = client.get_trail_status(Name=created_trail['Name'])
            except ClientError as err:
                module.fail_json(msg=err.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(err.response))
            if (enable_logging and (not status_resp['IsLogging'])):
                set_logging(module, client, name=ct_params['Name'], action='start')
            if ((not enable_logging) and status_resp['IsLogging']):
                set_logging(module, client, name=ct_params['Name'], action='stop')
            trail = get_trail_facts(module, client, ct_params['Name'])
        if module.check_mode:
            acct_id = '123456789012'
            try:
                sts_client = boto3_conn(module, conn_type='client', resource='sts', region=region, endpoint=ec2_url, **aws_connect_params)
                acct_id = sts_client.get_caller_identity()['Account']
            except ClientError:
                pass
            trail = dict()
            trail.update(ct_params)
            if ('EnableLogFileValidation' not in ct_params):
                ct_params['EnableLogFileValidation'] = False
            trail['EnableLogFileValidation'] = ct_params['EnableLogFileValidation']
            trail.pop('EnableLogFileValidation')
            fake_arn = ((((('arn:aws:cloudtrail:' + region) + ':') + acct_id) + ':trail/') + ct_params['Name'])
            trail['HasCustomEventSelectors'] = False
            trail['HomeRegion'] = region
            trail['TrailARN'] = fake_arn
            trail['IsLogging'] = enable_logging
            trail['tags'] = tags
        results['trail'] = camel_dict_to_snake_dict(trail)
    module.exit_json(**results)
