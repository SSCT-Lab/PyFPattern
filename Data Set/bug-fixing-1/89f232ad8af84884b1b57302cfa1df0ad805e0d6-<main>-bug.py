

def main():
    module = AnsibleModule(argument_spec=dict(bucket=dict(required=True), object=dict(default=None), src=dict(default=None), dest=dict(default=None), expiration=dict(default=600, aliases=['expiry']), mode=dict(choices=['get', 'put', 'delete', 'create', 'get_url', 'get_str'], required=True), permission=dict(choices=['private', 'public-read', 'authenticated-read'], default='private'), headers=dict(type='dict', default={
        
    }), gs_secret_key=dict(no_log=True, required=True), gs_access_key=dict(required=True), overwrite=dict(default=True, type='bool', aliases=['force'])))
    if (not HAS_BOTO):
        module.fail_json(msg='boto 2.9+ required for this module')
    bucket = module.params.get('bucket')
    obj = module.params.get('object')
    src = module.params.get('src')
    dest = module.params.get('dest')
    if dest:
        dest = os.path.expanduser(dest)
    mode = module.params.get('mode')
    expiry = module.params.get('expiration')
    gs_secret_key = module.params.get('gs_secret_key')
    gs_access_key = module.params.get('gs_access_key')
    overwrite = module.params.get('overwrite')
    if (mode == 'put'):
        if ((not src) or (not object)):
            module.fail_json(msg='When using PUT, src, bucket, object are mandatory parameters')
    if (mode == 'get'):
        if ((not dest) or (not object)):
            module.fail_json(msg='When using GET, dest, bucket, object are mandatory parameters')
    if obj:
        obj = os.path.expanduser(module.params['object'])
    try:
        gs = boto.connect_gs(gs_access_key, gs_secret_key)
    except boto.exception.NoAuthHandlerFound as e:
        module.fail_json(msg=str(e))
    if (mode == 'get'):
        if ((not bucket_check(module, gs, bucket)) or (not key_check(module, gs, bucket, obj))):
            module.fail_json(msg='Target bucket/key cannot be found', failed=True)
        if (not path_check(dest)):
            download_gsfile(module, gs, bucket, obj, dest)
        else:
            handle_get(module, gs, bucket, obj, overwrite, dest)
    if (mode == 'put'):
        if (not path_check(src)):
            module.fail_json(msg='Local object for PUT does not exist', failed=True)
        handle_put(module, gs, bucket, obj, overwrite, src, expiry)
    if (mode == 'delete'):
        handle_delete(module, gs, bucket, obj)
    if (mode == 'create'):
        handle_create(module, gs, bucket, obj)
    if (mode == 'get_url'):
        if (bucket and obj):
            if (bucket_check(module, gs, bucket) and key_check(module, gs, bucket, obj)):
                get_download_url(module, gs, bucket, obj, expiry)
            else:
                module.fail_json(msg='Key/Bucket does not exist', failed=True)
        else:
            module.fail_json(msg='Bucket and Object parameters must be set', failed=True)
    if (mode == 'get_str'):
        if (bucket and obj):
            if (bucket_check(module, gs, bucket) and key_check(module, gs, bucket, obj)):
                download_gsstr(module, gs, bucket, obj)
            else:
                module.fail_json(msg='Key/Bucket does not exist', failed=True)
        else:
            module.fail_json(msg='Bucket and Object parameters must be set', failed=True)
