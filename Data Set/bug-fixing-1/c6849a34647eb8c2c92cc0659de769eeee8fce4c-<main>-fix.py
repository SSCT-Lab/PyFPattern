

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(bucket=dict(required=True), dest=dict(default=None), encrypt=dict(default=True, type='bool'), expiry=dict(default=600, aliases=['expiration']), headers=dict(type='dict'), marker=dict(default=None), max_keys=dict(default=1000), metadata=dict(type='dict'), mode=dict(choices=['get', 'put', 'delete', 'create', 'geturl', 'getstr', 'delobj', 'list'], required=True), object=dict(), permission=dict(type='list', default=['private']), version=dict(default=None), overwrite=dict(aliases=['force'], default='always'), prefix=dict(default=None), retries=dict(aliases=['retry'], type='int', default=0), s3_url=dict(aliases=['S3_URL']), rgw=dict(default='no', type='bool'), src=dict(), ignore_nonexistent_bucket=dict(default=False, type='bool')))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module')
    bucket = module.params.get('bucket')
    encrypt = module.params.get('encrypt')
    expiry = int(module.params['expiry'])
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
    rgw = module.params.get('rgw')
    src = module.params.get('src')
    ignore_nonexistent_bucket = module.params.get('ignore_nonexistent_bucket')
    if dest:
        dest = os.path.expanduser(dest)
    for acl in module.params.get('permission'):
        if (acl not in CannedACLStrings):
            module.fail_json(msg=('Unknown permission specified: %s' % str(acl)))
    if (overwrite not in ['always', 'never', 'different']):
        if module.boolean(overwrite):
            overwrite = 'always'
        else:
            overwrite = 'never'
    (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module)
    if (region in ('us-east-1', '', None)):
        location = Location.DEFAULT
    else:
        location = region
    if module.params.get('object'):
        obj = module.params['object']
    if (obj and (mode == 'delete')):
        module.fail_json(msg='Parameter obj cannot be used with mode=delete')
    if ((not s3_url) and ('S3_URL' in os.environ)):
        s3_url = os.environ['S3_URL']
    if (rgw and (not s3_url)):
        module.fail_json(msg='rgw flavour requires s3_url')
    if ('.' in bucket):
        aws_connect_kwargs['calling_format'] = OrdinaryCallingFormat()
    try:
        s3 = get_s3_connection(aws_connect_kwargs, location, rgw, s3_url)
    except boto.exception.NoAuthHandlerFound as e:
        module.fail_json(msg=('No Authentication Handler found: %s ' % str(e)))
    except Exception as e:
        module.fail_json(msg=('Failed to connect to S3: %s' % str(e)))
    if (s3 is None):
        module.fail_json(msg='Unknown error, failed to create s3 connection, no information from boto.')
    bucketrtn = bucket_check(module, s3, bucket)
    if (not ignore_nonexistent_bucket):
        validate = True
        if ((mode not in ('create', 'put', 'delete')) and (not bucketrtn)):
            module.fail_json(msg='Source bucket cannot be found.')
    else:
        validate = False
    if (mode == 'get'):
        keyrtn = key_check(module, s3, bucket, obj, version=version, validate=validate)
        if (keyrtn is False):
            if (version is not None):
                module.fail_json(msg=('Key %s with version id %s does not exist.' % (obj, version)))
            else:
                module.fail_json(msg=('Key %s or source bucket %s does not exist.' % (obj, bucket)))
        pathrtn = path_check(dest)
        if (pathrtn is True):
            md5_remote = keysum(module, s3, bucket, obj, version=version, validate=validate)
            md5_local = module.md5(dest)
            if (md5_local == md5_remote):
                sum_matches = True
                if (overwrite == 'always'):
                    download_s3file(module, s3, bucket, obj, dest, retries, version=version, validate=validate)
                else:
                    module.exit_json(msg='Local and remote object are identical, ignoring. Use overwrite=always parameter to force.', changed=False)
            else:
                sum_matches = False
                if (overwrite in ('always', 'different')):
                    download_s3file(module, s3, bucket, obj, dest, retries, version=version, validate=validate)
                else:
                    module.exit_json(msg='WARNING: Checksums do not match. Use overwrite parameter to force download.')
        else:
            download_s3file(module, s3, bucket, obj, dest, retries, version=version, validate=validate)
        if (sum_matches and (overwrite == 'never')):
            module.exit_json(msg='Local and remote object are identical, ignoring. Use overwrite parameter to force.', changed=False)
    if (mode == 'put'):
        pathrtn = path_check(src)
        if (not pathrtn):
            module.fail_json(msg='Local object for PUT does not exist')
        if bucketrtn:
            keyrtn = key_check(module, s3, bucket, obj)
        if (bucketrtn and keyrtn):
            md5_remote = keysum(module, s3, bucket, obj)
            md5_local = module.md5(src)
            if (md5_local == md5_remote):
                sum_matches = True
                if (overwrite == 'always'):
                    upload_s3file(module, s3, bucket, obj, src, expiry, metadata, encrypt, headers)
                else:
                    get_download_url(module, s3, bucket, obj, expiry, changed=False)
            else:
                sum_matches = False
                if (overwrite in ('always', 'different')):
                    upload_s3file(module, s3, bucket, obj, src, expiry, metadata, encrypt, headers)
                else:
                    module.exit_json(msg='WARNING: Checksums do not match. Use overwrite parameter to force upload.')
        if (pathrtn and (not bucketrtn)):
            create_bucket(module, s3, bucket, location)
            upload_s3file(module, s3, bucket, obj, src, expiry, metadata, encrypt, headers)
        if (bucketrtn and pathrtn and (not keyrtn)):
            upload_s3file(module, s3, bucket, obj, src, expiry, metadata, encrypt, headers)
    if (mode == 'delobj'):
        if (obj is None):
            module.fail_json(msg='object parameter is required')
        if bucket:
            deletertn = delete_key(module, s3, bucket, obj, validate=validate)
            if (deletertn is True):
                module.exit_json(msg=('Object %s deleted from bucket %s.' % (obj, bucket)), changed=True)
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
        bucket_object = get_bucket(module, s3, bucket)
        if (bucket_object is None):
            module.fail_json(msg=('Target bucket (%s) cannot be found' % bucket))
        list_keys(module, bucket_object, prefix, marker, max_keys)
    if (mode == 'create'):
        if (bucket and (not obj)):
            if bucketrtn:
                module.exit_json(msg='Bucket already exists.', changed=False)
            else:
                module.exit_json(msg='Bucket created successfully', changed=create_bucket(module, s3, bucket, location))
        if (bucket and obj):
            if obj.endswith('/'):
                dirobj = obj
            else:
                dirobj = (obj + '/')
            if bucketrtn:
                keyrtn = key_check(module, s3, bucket, dirobj)
                if (keyrtn is True):
                    module.exit_json(msg=('Bucket %s and key %s already exists.' % (bucket, obj)), changed=False)
                else:
                    create_dirkey(module, s3, bucket, dirobj)
            else:
                created = create_bucket(module, s3, bucket, location)
                create_dirkey(module, s3, bucket, dirobj)
    if (mode == 'geturl'):
        if ((not bucket) and (not obj)):
            module.fail_json(msg='Bucket and Object parameters must be set')
        keyrtn = key_check(module, s3, bucket, obj, validate=validate)
        if keyrtn:
            get_download_url(module, s3, bucket, obj, expiry, validate=validate)
        else:
            module.fail_json(msg=('Key %s does not exist.' % obj))
    if (mode == 'getstr'):
        if (bucket and obj):
            keyrtn = key_check(module, s3, bucket, obj, version=version, validate=validate)
            if keyrtn:
                download_s3str(module, s3, bucket, obj, version=version, validate=validate)
            elif (version is not None):
                module.fail_json(msg=('Key %s with version id %s does not exist.' % (obj, version)))
            else:
                module.fail_json(msg=('Key %s does not exist.' % obj))
    module.exit_json(failed=False)
