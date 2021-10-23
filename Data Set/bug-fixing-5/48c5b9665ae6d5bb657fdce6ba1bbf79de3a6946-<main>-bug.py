def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(mode=dict(choices=['push'], default='push'), file_change_strategy=dict(choices=['force', 'date_size', 'checksum'], default='date_size'), bucket=dict(required=True), key_prefix=dict(required=False, default=''), file_root=dict(required=True, type='path'), permission=dict(required=False, choices=['private', 'public-read', 'public-read-write', 'authenticated-read', 'aws-exec-read', 'bucket-owner-read', 'bucket-owner-full-control']), retries=dict(required=False), mime_map=dict(required=False, type='dict'), exclude=dict(required=False, default='.*'), include=dict(required=False, default='*'), cache_control=dict(required=False, default='')))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 required for this module')
    result = {
        
    }
    mode = module.params['mode']
    (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
    if (not region):
        module.fail_json(msg='Region must be specified')
    s3 = boto3_conn(module, conn_type='client', resource='s3', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    if (mode == 'push'):
        try:
            result['filelist_initial'] = gather_files(module.params['file_root'], exclude=module.params['exclude'], include=module.params['include'])
            result['filelist_typed'] = determine_mimetypes(result['filelist_initial'], module.params.get('mime_map'))
            result['filelist_s3'] = calculate_s3_path(result['filelist_typed'], module.params['key_prefix'])
            result['filelist_local_etag'] = calculate_local_etag(result['filelist_s3'])
            result['filelist_actionable'] = filter_list(s3, module.params['bucket'], result['filelist_local_etag'], module.params['file_change_strategy'])
            result['uploads'] = upload_files(s3, module.params['bucket'], result['filelist_actionable'], module.params)
            if (result.get('uploads') and len(result.get('uploads'))):
                result['changed'] = True
        except botocore.exceptions.ClientError as err:
            error_msg = boto_exception(err)
            module.fail_json(msg=error_msg, exception=traceback.format_exc(), **camel_dict_to_snake_dict(err.response))
    module.exit_json(**result)