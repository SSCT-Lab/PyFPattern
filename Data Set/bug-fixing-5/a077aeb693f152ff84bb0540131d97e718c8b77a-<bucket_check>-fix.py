def bucket_check(module, s3, bucket, validate=True):
    try:
        result = s3.lookup(bucket, validate=validate)
    except s3.provider.storage_response_error as e:
        module.fail_json(msg=('Failed while looking up bucket (during bucket_check) %s: %s' % (bucket, e)), exception=traceback.format_exc())
    return bool(result)