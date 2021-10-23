

def download_s3file(module, s3, bucket, obj, dest, retries, version=None):
    if module.check_mode:
        module.exit_json(msg='GET operation skipped - running in check mode', changed=True)
    try:
        if version:
            key = s3.get_object(Bucket=bucket, Key=obj, VersionId=version)
        else:
            key = s3.get_object(Bucket=bucket, Key=obj)
    except botocore.exceptions.ClientError as e:
        if ((e.response['Error']['Code'] == 'InvalidArgument') and ('require AWS Signature Version 4' in to_text(e))):
            raise Sigv4Required()
        elif (e.response['Error']['Code'] not in ('403', '404')):
            module.fail_json_aws(e, msg=('Could not find the key %s.' % obj))
    except botocore.exceptions.BotoCoreError as e:
        module.fail_json_aws(e, msg=('Could not find the key %s.' % obj))
    optional_kwargs = ({
        'ExtraArgs': {
            'VersionId': version,
        },
    } if version else {
        
    })
    for x in range(0, (retries + 1)):
        try:
            s3.download_file(bucket, obj, dest, **optional_kwargs)
            module.exit_json(msg='GET operation complete', changed=True)
        except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
            if (x >= retries):
                module.fail_json_aws(e, msg=('Failed while downloading %s.' % obj))
        except SSLError as e:
            if (x >= retries):
                module.fail_json_aws(e, msg='s3 download failed')
