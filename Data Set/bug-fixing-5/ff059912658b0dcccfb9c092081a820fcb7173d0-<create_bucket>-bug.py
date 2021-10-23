def create_bucket(module, s3, bucket, location=None):
    if module.check_mode:
        module.exit_json(msg='CREATE operation skipped - running in check mode', changed=True)
    configuration = {
        
    }
    if (location not in ('us-east-1', None)):
        configuration['LocationConstraint'] = location
    try:
        if (len(configuration) > 0):
            s3.create_bucket(Bucket=bucket, CreateBucketConfiguration=configuration)
        else:
            s3.create_bucket(Bucket=bucket)
        if (module.params.get('permission') and (not module.params.get('ignore_nonexistent_bucket'))):
            s3.get_waiter('bucket_exists').wait(Bucket=bucket)
        for acl in module.params.get('permission'):
            s3.put_bucket_acl(ACL=acl, Bucket=bucket)
    except botocore.exceptions.ClientError as e:
        if (e.response['Error']['Code'] in IGNORE_S3_DROP_IN_EXCEPTIONS):
            module.warn('PutBucketAcl is not implemented by your storage provider. Set the permission parameters to the empty list to avoid this warning')
        else:
            module.fail_json_aws(e, msg='Failed while creating bucket or setting acl (check that you have CreateBucket and PutBucketAcl permission).')
    except botocore.exceptions.BotoCoreError as e:
        module.fail_json_aws(e, msg='Failed while creating bucket or setting acl (check that you have CreateBucket and PutBucketAcl permission).')
    if bucket:
        return True