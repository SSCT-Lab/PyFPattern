def upload_s3file(module, s3, bucket, obj, src, expiry, metadata, encrypt, headers):
    try:
        bucket = s3.lookup(bucket)
        key = bucket.new_key(obj)
        if metadata:
            for meta_key in metadata.keys():
                key.set_metadata(meta_key, metadata[meta_key])
        key.set_contents_from_filename(src, encrypt_key=encrypt, headers=headers)
        for acl in module.params.get('permission'):
            key.set_acl(acl)
        url = key.generate_url(expiry)
        module.exit_json(msg='PUT operation complete', url=url, changed=True)
    except s3.provider.storage_copy_error as e:
        module.fail_json(msg=str(e))