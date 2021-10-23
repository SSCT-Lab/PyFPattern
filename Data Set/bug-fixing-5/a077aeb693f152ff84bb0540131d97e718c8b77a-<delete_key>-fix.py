def delete_key(module, s3, bucket, obj, validate=True):
    try:
        bucket = s3.lookup(bucket, validate=validate)
        bucket.delete_key(obj)
        module.exit_json(msg=('Object deleted from bucket %s' % bucket), changed=True)
    except s3.provider.storage_response_error as e:
        module.fail_json(msg=str(e))