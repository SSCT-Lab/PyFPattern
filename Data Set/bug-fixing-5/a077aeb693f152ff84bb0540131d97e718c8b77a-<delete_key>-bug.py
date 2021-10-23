def delete_key(module, s3, bucket, obj):
    try:
        bucket = s3.lookup(bucket)
        bucket.delete_key(obj)
        module.exit_json(msg=('Object deleted from bucket %s' % bucket), changed=True)
    except s3.provider.storage_response_error as e:
        module.fail_json(msg=str(e))