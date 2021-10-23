def download_s3str(module, s3, bucket, obj, version=None, validate=True):
    try:
        bucket = s3.lookup(bucket, validate=validate)
        key = bucket.get_key(obj, version_id=version)
        contents = key.get_contents_as_string()
        module.exit_json(msg='GET operation complete', contents=contents, changed=True)
    except s3.provider.storage_copy_error as e:
        module.fail_json(msg=str(e))