def download_s3file(module, s3, bucket, obj, dest, retries, version=None, validate=True):
    bucket = s3.lookup(bucket, validate=validate)
    key = bucket.get_key(obj, version_id=version)
    for x in range(0, (retries + 1)):
        try:
            key.get_contents_to_filename(dest)
            module.exit_json(msg='GET operation complete', changed=True)
        except s3.provider.storage_copy_error as e:
            module.fail_json(msg=str(e))
        except SSLError as e:
            if (x >= retries):
                module.fail_json(msg=('s3 download failed; %s' % e))
            pass