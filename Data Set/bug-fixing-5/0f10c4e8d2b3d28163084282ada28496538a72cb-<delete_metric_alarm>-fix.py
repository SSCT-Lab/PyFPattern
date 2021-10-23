def delete_metric_alarm(connection, module):
    name = module.params.get('name')
    alarms = None
    try:
        alarms = connection.describe_alarms(alarm_names=[name])
    except BotoServerError as e:
        module.fail_json(msg=('Failed to describe alarm %s: %s' % (name, str(e))), exception=traceback.format_exc())
    if alarms:
        try:
            connection.delete_alarms([name])
            module.exit_json(changed=True)
        except BotoServerError as e:
            module.fail_json(msg=str(e))
    else:
        module.exit_json(changed=False)