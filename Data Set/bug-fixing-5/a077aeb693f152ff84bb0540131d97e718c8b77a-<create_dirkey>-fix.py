def create_dirkey(module, s3, bucket, obj, validate=True):
    try:
        bucket = s3.lookup(bucket, validate=validate)
        key = bucket.new_key(obj)
        key.set_contents_from_string('')
        module.exit_json(msg=('Virtual directory %s created in bucket %s' % (obj, bucket.name)), changed=True)
    except s3.provider.storage_response_error as e:
        module.fail_json(msg=str(e))