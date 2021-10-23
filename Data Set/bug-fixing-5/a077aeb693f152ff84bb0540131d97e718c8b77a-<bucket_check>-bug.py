def bucket_check(module, s3, bucket):
    try:
        result = s3.lookup(bucket)
    except s3.provider.storage_response_error as e:
        module.fail_json(msg=str(e))
    if result:
        return True
    else:
        return False