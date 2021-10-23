def key_check(module, s3, bucket, obj, version=None):
    try:
        bucket = s3.lookup(bucket)
        key_check = bucket.get_key(obj, version_id=version)
    except s3.provider.storage_response_error as e:
        if ((version is not None) and (e.status == 400)):
            key_check = None
        else:
            module.fail_json(msg=str(e))
    if key_check:
        return True
    else:
        return False