

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(bucket=dict(required=True), dest=dict(default=None, type='path'), encrypt=dict(default=True, type='bool'), encryption_mode=dict(choices=['AES256', 'aws:kms'], default='AES256'), expiry=dict(default=600, type='int', aliases=['expiration']), headers=dict(type='dict'), marker=dict(default=''), max_keys=dict(default=1000, type='int'), metadata=dict(type='dict'), mode=dict(choices=['get', 'put', 'delete', 'create', 'geturl', 'getstr', 'delobj', 'list'], required=True), object=dict(), permission=dict(type='list', default=['private']), version=dict(default=None), overwrite=dict(aliases=['force'], default='always'), prefix=dict(default=''), retries=dict(aliases=['retry'], type='int', default=0), s3_url=dict(aliases=['S3_URL']), dualstack=dict(default='no', type='bool'), rgw=dict(default='no', type='bool'), src=dict(), ignore_nonexistent_bucket=dict(default=False, type='bool'), encryption_kms_key_id=dict()))
    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[['mode', 'put', ['src', 'object']], ['mode', 'get', ['dest', 'object']], ['mode', 'getstr', ['object']], ['mode', 'geturl', ['object']]])
    if (module._name == 's3'):
        module.deprecate("The 's3' module is being renamed 'aws_s3'", version=2.7)
    bucket = module.params.get('bucket')
    encrypt = module.params.get('encrypt')
    expiry = module.params.get('expiry')
    dest = module.params.get('dest', '')
    headers = module.params.get('headers')
    marker = module.params.get('marker')
    max_keys = module.params.get('max_keys')
    metadata = module.params.get('metadata')
    mode = module.params.get('mode')
    obj = module.params.get('object')
    version = module.params.get('version')
    overwrite = module.params.get('overwrite')
    prefix = module.params.get('prefix')
    retries = module.params.get('retries')
    s3_url = module.params.get('s3_url')
    dualstack = module.params.get('dualstack')
    rgw = module.params.get('rgw')
    src = module.params.get('src')
    ignore_nonexistent_bucket = module.params.get('ignore_nonexistent_bucket')
    object_canned_acl = ['private', 'public-read', 'public-read-write', 'aws-exec-read', 'authenticated-read', 'bucket-owner-read', 'bucket-owner-full-control']
    bucket_canned_acl = ['private', 'public-read', 'public-read-write', 'authenticated-read']
    if (overwrite not in ['always', 'never', 'different']):
        if module.boolean(overwrite):
            overwrite = 'always'
        else:
            overwrite = 'never'
    (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
    if (region in ('us-east-1', '', None)):
        location = 'us-east-1'
    else:
        location = region
    if module.params.get('object'):
        obj = module.params['object']
        if obj.startswith('/'):
            obj = obj[1:]
    if (obj and (mode == 'delete')):
        module.fail_json(msg='Parameter obj cannot be used with mode=delete')
    if ((not s3_url) and ('S3_URL' in os.environ)):
        s3_url = os.environ['S3_URL']
    if (dualstack and (s3_url is not None) and ('amazonaws.com' not in s3_url)):
        module.fail_json(msg='dualstack only applies to AWS S3')
    if (dualstack and (not module.botocore_at_least('1.4.45'))):
        module.fail_json(msg='dualstack requires botocore >= 1.4.45')
    if (rgw and (not s3_url)):
        module.fail_json(msg='rgw flavour requires s3_url')
    if s3_url:
        for key in ['validate_certs', 'security_token', 'profile_name']:
            aws_connect_kwargs.pop(key, None)
    s3 = get_s3_connection(module, aws_connect_kwargs, location, rgw, s3_url)
    validate = (not ignore_nonexistent_bucket)
    bucket_acl = [acl for acl in module.params.get('permission') if (acl in bucket_canned_acl)]
    object_acl = [acl for acl in module.params.get('permission') if (acl in object_canned_acl)]
    error_acl = [acl for acl in module.params.get('permission') if ((acl not in bucket_canned_acl) and (acl not in object_canned_acl))]
    if error_acl:
        module.fail_json(msg=('Unknown permission specified: %s' % error_acl))
    bucketrtn = bucket_check(module, s3, bucket, validate=validate)
    if (validate and (mode not in ('create', 'put', 'delete')) and (not bucketrtn)):
        module.fail_json(msg='Source bucket cannot be found.')
    if (mode == 'get'):
        keyrtn = key_check(module, s3, bucket, obj, version=version, validate=validate)
        if (keyrtn is False):
            if version:
                module.fail_json(msg=('Key %s with version id %s does not exist.' % (obj, version)))
            else:
                module.fail_json(msg=('Key %s does not exist.' % obj))
        if path_check(dest):
            if keysum_compare(module, dest, s3, bucket, obj, version=version):
                sum_matches = True
                if (overwrite == 'always'):
                    try:
                        download_s3file(module, s3, bucket, obj, dest, retries, version=version)
                    except Sigv4Required:
                        s3 = get_s3_connection(module, aws_connect_kwargs, location, rgw, s3_url, sig_4=True)
                        download_s3file(module, s3, bucket, obj, dest, retries, version=version)
                else:
                    module.exit_json(msg='Local and remote object are identical, ignoring. Use overwrite=always parameter to force.', changed=False)
            else:
                sum_matches = False
                if (overwrite in ('always', 'different')):
                    try:
                        download_s3file(module, s3, bucket, obj, dest, retries, version=version)
                    except Sigv4Required:
                        s3 = get_s3_connection(module, aws_connect_kwargs, location, rgw, s3_url, sig_4=True)
                        download_s3file(module, s3, bucket, obj, dest, retries, version=version)
                else:
                    module.exit_json(msg='WARNING: Checksums do not match. Use overwrite parameter to force download.')
        else:
            try:
                download_s3file(module, s3, bucket, obj, dest, retries, version=version)
            except Sigv4Required:
                s3 = get_s3_connection(module, aws_connect_kwargs, location, rgw, s3_url, sig_4=True)
                download_s3file(module, s3, bucket, obj, dest, retries, version=version)
    if (mode == 'put'):
        if (not path_check(src)):
            module.fail_json(msg='Local object for PUT does not exist')
        if bucketrtn:
            keyrtn = key_check(module, s3, bucket, obj, version=version, validate=validate)
        if (bucketrtn and keyrtn):
            if keysum_compare(module, src, s3, bucket, obj):
                sum_matches = True
                if (overwrite == 'always'):
                    module.params['permission'] = object_acl
                    upload_s3file(module, s3, bucket, obj, src, expiry, metadata, encrypt, headers)
                else:
                    get_download_url(module, s3, bucket, obj, expiry, changed=False)
            else:
                sum_matches = False
                if (overwrite in ('always', 'different')):
                    module.params['permission'] = object_acl
                    upload_s3file(module, s3, bucket, obj, src, expiry, metadata, encrypt, headers)
                else:
                    module.exit_json(msg='WARNING: Checksums do not match. Use overwrite parameter to force upload.')
        if (not bucketrtn):
            module.params['permission'] = bucket_acl
            create_bucket(module, s3, bucket, location)
            module.params['permission'] = object_acl
            upload_s3file(module, s3, bucket, obj, src, expiry, metadata, encrypt, headers)
        if (bucketrtn and (not keyrtn)):
            module.params['permission'] = object_acl
            upload_s3file(module, s3, bucket, obj, src, expiry, metadata, encrypt, headers)
    if (mode == 'delobj'):
        if (obj is None):
            module.fail_json(msg='object parameter is required')
        if bucket:
            deletertn = delete_key(module, s3, bucket, obj)
            if (deletertn is True):
                module.exit_json(msg=('Object deleted from bucket %s.' % bucket), changed=True)
        else:
            module.fail_json(msg='Bucket parameter is required.')
    if (mode == 'delete'):
        if bucket:
            deletertn = delete_bucket(module, s3, bucket)
            if (deletertn is True):
                module.exit_json(msg=('Bucket %s and all keys have been deleted.' % bucket), changed=True)
        else:
            module.fail_json(msg='Bucket parameter is required.')
    if (mode == 'list'):
        exists = bucket_check(module, s3, bucket)
        if (not exists):
            module.fail_json(msg=('Target bucket (%s) cannot be found' % bucket))
        list_keys(module, s3, bucket, prefix, marker, max_keys)
    if (mode == 'create'):
        if (bucket and (not obj)):
            if bucketrtn:
                module.exit_json(msg='Bucket already exists.', changed=False)
            else:
                module.params['permission'] = bucket_acl
                module.exit_json(msg='Bucket created successfully', changed=create_bucket(module, s3, bucket, location))
        if (bucket and obj):
            if obj.endswith('/'):
                dirobj = obj
            else:
                dirobj = (obj + '/')
            if bucketrtn:
                if key_check(module, s3, bucket, dirobj):
                    module.exit_json(msg=('Bucket %s and key %s already exists.' % (bucket, obj)), changed=False)
                else:
                    module.params['permission'] = object_acl
                    create_dirkey(module, s3, bucket, dirobj, encrypt)
            else:
                module.params['permission'] = bucket_acl
                created = create_bucket(module, s3, bucket, location)
                module.params['permission'] = object_acl
                create_dirkey(module, s3, bucket, dirobj, encrypt)
    if (mode == 'geturl'):
        if ((not bucket) and (not obj)):
            module.fail_json(msg='Bucket and Object parameters must be set')
        keyrtn = key_check(module, s3, bucket, obj, version=version, validate=validate)
        if keyrtn:
            get_download_url(module, s3, bucket, obj, expiry)
        else:
            module.fail_json(msg=('Key %s does not exist.' % obj))
    if (mode == 'getstr'):
        if (bucket and obj):
            keyrtn = key_check(module, s3, bucket, obj, version=version, validate=validate)
            if keyrtn:
                try:
                    download_s3str(module, s3, bucket, obj, version=version)
                except Sigv4Required:
                    s3 = get_s3_connection(module, aws_connect_kwargs, location, rgw, s3_url, sig_4=True)
                    download_s3str(module, s3, bucket, obj, version=version)
            elif (version is not None):
                module.fail_json(msg=('Key %s with version id %s does not exist.' % (obj, version)))
            else:
                module.fail_json(msg=('Key %s does not exist.' % obj))
    module.exit_json(failed=False)
