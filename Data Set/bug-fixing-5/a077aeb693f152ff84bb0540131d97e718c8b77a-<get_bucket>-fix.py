def get_bucket(module, s3, bucket):
    try:
        return s3.lookup(bucket)
    except s3.provider.storage_response_error as e:
        module.fail_json(msg=('Failed while getting bucket %s: %s' % (bucket, e)), exception=traceback.format_exc())