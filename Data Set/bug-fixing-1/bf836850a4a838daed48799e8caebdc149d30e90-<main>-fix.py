

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(bucket=dict(required=True), dest=dict(default=None, type='path'), encrypt=dict(default=True, type='bool'), expiry=dict(default=600, aliases=['expiration']), headers=dict(type='dict'), marker=dict(default=None), max_keys=dict(default=1000), metadata=dict(type='dict'), mode=dict(choices=['get', 'put', 'delete', 'create', 'geturl', 'getstr', 'delobj', 'list'], required=True), object=dict(type='path'), permission=dict(type='list', default=['private']), version=dict(default=None), overwrite=dict(aliases=['force'], default='always'), prefix=dict(default=None), retries=dict(aliases=['retry'], type='int', default=0), s3_url=dict(aliases=['S3_URL']), rgw=dict(default='no', type='bool'), src=dict()))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module')
    bucket = module.params.get('bucket')
    encrypt = module.params.get('encrypt')
    expiry = int(module.params['expiry'])
    if module.params.get('dest'):
        dest = module.params.get('dest')
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
    if (mode == 'get'):
        bucketrtn = bucket_check(module, s3, bucket)
        if (bucketrtn is False):
            module.fail_json(msg='Source bucket cannot be found', failed=True)
        keyrtn = key_check(module, s3, bucket, obj, version=version)
        if (keyrtn is False):
            if (version is not None):
                module.fail_json(msg=('Key %s with version id %s does not exist.' % (obj, version)), failed=True)
            else:
                module.fail_json(msg=('Key %s does not exist.' % obj), failed=True)
        pathrtn = path_check(dest)
        if ((pathrtn is False) or (overwrite == 'always')):
            download_s3file(module, s3, bucket, obj, dest, retries, version=version)
        if (pathrtn is True):
            md5_remote = keysum(module, s3, bucket, obj, version=version)
            md5_local = module.md5(dest)
            if (md5_local == md5_remote):
                sum_matches = True
                if (overwrite == 'always'):
                    download_s3file(module, s3, bucket, obj, dest, retries, version=version)
                else:
                    module.exit_json(msg='Local and remote object are identical, ignoring. Use overwrite=always parameter to force.', changed=False)
            else:
                sum_matches = False
                if (overwrite in ('always', 'different')):
                    download_s3file(module, s3, bucket, obj, dest, retries, version=version)
                else:
                    module.exit_json(msg='WARNING: Checksums do not match. Use overwrite parameter to force download.')
        if ((sum_matches is True) and (overwrite == 'never')):
            module.exit_json(msg='Local and remote object are identical, ignoring. Use overwrite parameter to force.', changed=False)
    if (mode == 'put'):
        pathrtn = path_check(src)
        if (pathrtn is False):
            module.fail_json(msg='Local object for PUT does not exist', failed=True)
        bucketrtn = bucket_check(module, s3, bucket)
        if (bucketrtn is True):
            keyrtn = key_check(module, s3, bucket, obj)
        if ((bucketrtn is True) and (keyrtn is True)):
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
        if ((bucketrtn is False) and (pathrtn is True)):
            create_bucket(module, s3, bucket, location)
            upload_s3file(module, s3, bucket, obj, src, expiry, metadata, encrypt, headers)
        if ((bucketrtn is True) and (pathrtn is True) and (keyrtn is False)):
            upload_s3file(module, s3, bucket, obj, src, expiry, metadata, encrypt, headers)
    if (mode == 'delobj'):
        if (obj is None):
            module.fail_json(msg='object parameter is required', failed=True)
        if bucket:
            bucketrtn = bucket_check(module, s3, bucket)
            if (bucketrtn is True):
                deletertn = delete_key(module, s3, bucket, obj)
                if (deletertn is True):
                    module.exit_json(msg=('Object %s deleted from bucket %s.' % (obj, bucket)), changed=True)
            else:
                module.fail_json(msg='Bucket does not exist.', changed=False)
        else:
            module.fail_json(msg='Bucket parameter is required.', failed=True)
    if (mode == 'delete'):
        if bucket:
            bucketrtn = bucket_check(module, s3, bucket)
            if (bucketrtn is True):
                deletertn = delete_bucket(module, s3, bucket)
                if (deletertn is True):
                    module.exit_json(msg=('Bucket %s and all keys have been deleted.' % bucket), changed=True)
            else:
                module.fail_json(msg='Bucket does not exist.', changed=False)
        else:
            module.fail_json(msg='Bucket parameter is required.', failed=True)
    if (mode == 'list'):
        bucket_object = get_bucket(module, s3, bucket)
        if (bucket_object is None):
            module.fail_json(msg=('Target bucket (%s) cannot be found' % bucket), failed=True)
        list_keys(module, bucket_object, prefix, marker, max_keys)
    if (mode == 'create'):
        if (bucket and (not obj)):
            bucketrtn = bucket_check(module, s3, bucket)
            if (bucketrtn is True):
                module.exit_json(msg='Bucket already exists.', changed=False)
            else:
                module.exit_json(msg='Bucket created successfully', changed=create_bucket(module, s3, bucket, location))
        if (bucket and obj):
            bucketrtn = bucket_check(module, s3, bucket)
            if obj.endswith('/'):
                dirobj = obj
            else:
                dirobj = (obj + '/')
            if (bucketrtn is True):
                keyrtn = key_check(module, s3, bucket, dirobj)
                if (keyrtn is True):
                    module.exit_json(msg=('Bucket %s and key %s already exists.' % (bucket, obj)), changed=False)
                else:
                    create_dirkey(module, s3, bucket, dirobj)
            if (bucketrtn is False):
                created = create_bucket(module, s3, bucket, location)
                create_dirkey(module, s3, bucket, dirobj)
    if (mode == 'geturl'):
        if (bucket and obj):
            bucketrtn = bucket_check(module, s3, bucket)
            if (bucketrtn is False):
                module.fail_json(msg=('Bucket %s does not exist.' % bucket), failed=True)
            else:
                keyrtn = key_check(module, s3, bucket, obj)
                if (keyrtn is True):
                    get_download_url(module, s3, bucket, obj, expiry)
                else:
                    module.fail_json(msg=('Key %s does not exist.' % obj), failed=True)
        else:
            module.fail_json(msg='Bucket and Object parameters must be set', failed=True)
    if (mode == 'getstr'):
        if (bucket and obj):
            bucketrtn = bucket_check(module, s3, bucket)
            if (bucketrtn is False):
                module.fail_json(msg=('Bucket %s does not exist.' % bucket), failed=True)
            else:
                keyrtn = key_check(module, s3, bucket, obj, version=version)
                if (keyrtn is True):
                    download_s3str(module, s3, bucket, obj, version=version)
                elif (version is not None):
                    module.fail_json(msg=('Key %s with version id %s does not exist.' % (obj, version)), failed=True)
                else:
                    module.fail_json(msg=('Key %s does not exist.' % obj), failed=True)
    module.exit_json(failed=False)
