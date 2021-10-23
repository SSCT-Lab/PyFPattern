def wait_versioning_is_applied(module, s3_client, bucket_name, required_versioning):
    for dummy in range(0, 24):
        try:
            versioning_status = get_bucket_versioning(s3_client, bucket_name)
        except (BotoCoreError, ClientError) as e:
            module.fail_json_aws(e, msg='Failed to get updated versioning for bucket')
        if (versioning_status.get('Status') != required_versioning):
            time.sleep(5)
        else:
            return versioning_status
    module.fail_json(msg='Bucket versioning failed to apply in the expected time')