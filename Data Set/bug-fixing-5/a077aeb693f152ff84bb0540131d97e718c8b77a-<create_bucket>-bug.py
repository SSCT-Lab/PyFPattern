def create_bucket(module, s3, bucket, location=None):
    if (location is None):
        location = Location.DEFAULT
    try:
        bucket = s3.create_bucket(bucket, location=location)
        for acl in module.params.get('permission'):
            bucket.set_acl(acl)
    except s3.provider.storage_response_error as e:
        module.fail_json(msg=str(e))
    if bucket:
        return True