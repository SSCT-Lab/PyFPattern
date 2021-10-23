def delete_bucket(module, s3, bucket):
    if module.check_mode:
        module.exit_json(msg='DELETE operation skipped - running in check mode', changed=True)
    try:
        exists = bucket_check(module, s3, bucket)
        if (exists is False):
            return False
        keys = [{
            'Key': key,
        } for key in paginated_list(s3, Bucket=bucket)]
        if keys:
            s3.delete_objects(Bucket=bucket, Delete={
                'Objects': keys,
            })
        s3.delete_bucket(Bucket=bucket)
        return True
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg='Failed while deleting bucket %s.', exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))