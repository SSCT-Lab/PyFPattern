def upload_s3file(module, s3, bucket, obj, src, expiry, metadata, encrypt, headers):
    if module.check_mode:
        module.exit_json(msg='PUT operation skipped - running in check mode', changed=True)
    try:
        extra = {
            
        }
        if encrypt:
            extra['ServerSideEncryption'] = 'AES256'
        if metadata:
            extra['Metadata'] = {
                
            }
            for option in metadata:
                extra_args_option = option_in_extra_args(option)
                if (extra_args_option is not None):
                    extra[extra_args_option] = metadata[option]
                else:
                    extra['Metadata'][option] = metadata[option]
        if ('ContentType' not in extra):
            content_type = mimetypes.guess_type(src)[0]
            if (content_type is None):
                content_type = 'binary/octet-stream'
            extra['ContentType'] = content_type
        s3.upload_file(Filename=src, Bucket=bucket, Key=obj, ExtraArgs=extra)
        for acl in module.params.get('permission'):
            s3.put_object_acl(ACL=acl, Bucket=bucket, Key=obj)
        url = s3.generate_presigned_url(ClientMethod='put_object', Params={
            'Bucket': bucket,
            'Key': obj,
        }, ExpiresIn=expiry)
        module.exit_json(msg='PUT operation complete', url=url, changed=True)
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg='Unable to complete PUT operation.', exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))