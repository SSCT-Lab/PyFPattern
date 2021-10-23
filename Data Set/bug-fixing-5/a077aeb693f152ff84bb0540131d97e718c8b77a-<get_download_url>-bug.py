def get_download_url(module, s3, bucket, obj, expiry, changed=True):
    try:
        bucket = s3.lookup(bucket)
        key = bucket.lookup(obj)
        url = key.generate_url(expiry)
        module.exit_json(msg='Download url:', url=url, expiry=expiry, changed=changed)
    except s3.provider.storage_response_error as e:
        module.fail_json(msg=str(e))