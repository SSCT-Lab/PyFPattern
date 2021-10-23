def destroy_bucket(s3_client, module):
    force = module.params.get('force')
    name = module.params.get('name')
    try:
        bucket_is_present = bucket_exists(s3_client, name)
    except EndpointConnectionError as e:
        module.fail_json_aws(e, msg=('Invalid endpoint provided: %s' % to_text(e)))
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to check bucket presence')
    if (not bucket_is_present):
        module.exit_json(changed=False)
    if force:
        try:
            for keys in paginated_list(s3_client, Bucket=name):
                formatted_keys = [{
                    'Key': key,
                } for key in keys]
                if formatted_keys:
                    s3_client.delete_objects(Bucket=name, Delete={
                        'Objects': formatted_keys,
                    })
        except (BotoCoreError, ClientError) as e:
            module.fail_json_aws(e, msg='Failed while deleting bucket')
    try:
        delete_bucket(s3_client, name)
        s3_client.get_waiter('bucket_not_exists').wait(Bucket=name)
    except WaiterError as e:
        module.fail_json_aws(e, msg='An error occurred waiting for the bucket to be deleted.')
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to delete bucket')
    module.exit_json(changed=True)