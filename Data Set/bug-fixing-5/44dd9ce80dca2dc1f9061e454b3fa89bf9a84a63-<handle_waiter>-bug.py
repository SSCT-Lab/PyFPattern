def handle_waiter(conn, module, waiter_name, params, start_time):
    params['WaiterConfig'] = wait_config(module.params['wait_timeout'], start_time)
    try:
        get_waiter(conn, waiter_name).wait(**params)
    except botocore.exceptions.WaiterError as e:
        module.fail_json_aws(e, 'Failed to wait for updates to complete')
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        module.fail_json_aws(e, 'An exception happened while trying to wait for updates')