def keysum(module, s3, bucket, obj, version=None):
    bucket = s3.lookup(bucket)
    key_check = bucket.get_key(obj, version_id=version)
    if (not key_check):
        return None
    md5_remote = key_check.etag[1:(- 1)]
    etag_multipart = ('-' in md5_remote)
    if (etag_multipart is True):
        module.fail_json(msg='Files uploaded with multipart of s3 are not supported with checksum, unable to compute checksum.')
    return md5_remote