

def upload_files(s3, bucket, filelist, params):
    ret = []
    for entry in filelist:
        args = {
            'ContentLength': entry['bytes'],
            'ContentType': entry['mime_type'],
        }
        if params.get('permission'):
            args['ACL'] = params['permission']
        s3.upload_file(entry['fullpath'], bucket, entry['s3_path'], ExtraArgs=None, Callback=None, Config=None)
        ret.append(entry)
    return ret
