def handle_waiter(conn, module, waiter_name, params, start_time):
    try:
        get_waiter(conn, waiter_name).wait(**waiter_params(module, params, start_time))
    except botocore.exceptions.WaiterError as e:
        module.fail_json_aws(e, 'Failed to wait for updates to complete')
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        module.fail_json_aws(e, 'An exception happened while trying to wait for updates')