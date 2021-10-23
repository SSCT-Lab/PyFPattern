def create_metric_alarm(connection, module):
    name = module.params.get('name')
    metric = module.params.get('metric')
    namespace = module.params.get('namespace')
    statistic = module.params.get('statistic')
    comparison = module.params.get('comparison')
    threshold = module.params.get('threshold')
    period = module.params.get('period')
    evaluation_periods = module.params.get('evaluation_periods')
    unit = module.params.get('unit')
    description = module.params.get('description')
    dimensions = module.params.get('dimensions')
    alarm_actions = module.params.get('alarm_actions')
    insufficient_data_actions = module.params.get('insufficient_data_actions')
    ok_actions = module.params.get('ok_actions')
    alarms = connection.describe_alarms(alarm_names=[name])
    if (not alarms):
        alm = MetricAlarm(name=name, metric=metric, namespace=namespace, statistic=statistic, comparison=comparison, threshold=threshold, period=period, evaluation_periods=evaluation_periods, unit=unit, description=description, dimensions=dimensions, alarm_actions=alarm_actions, insufficient_data_actions=insufficient_data_actions, ok_actions=ok_actions)
        try:
            connection.create_alarm(alm)
            changed = True
            alarms = connection.describe_alarms(alarm_names=[name])
        except BotoServerError as e:
            module.fail_json(msg=str(e))
    else:
        alarm = alarms[0]
        changed = False
        for attr in ('comparison', 'metric', 'namespace', 'statistic', 'threshold', 'period', 'evaluation_periods', 'unit', 'description'):
            if (getattr(alarm, attr) != module.params.get(attr)):
                changed = True
                setattr(alarm, attr, module.params.get(attr))
        comparison = alarm.comparison
        comparisons = {
            '<=': 'LessThanOrEqualToThreshold',
            '<': 'LessThanThreshold',
            '>=': 'GreaterThanOrEqualToThreshold',
            '>': 'GreaterThanThreshold',
        }
        alarm.comparison = comparisons[comparison]
        dim1 = module.params.get('dimensions')
        dim2 = alarm.dimensions
        for keys in dim1:
            if (not isinstance(dim1[keys], list)):
                dim1[keys] = [dim1[keys]]
            if ((keys not in dim2) or (dim1[keys] != dim2[keys])):
                changed = True
                setattr(alarm, 'dimensions', dim1)
        for attr in ('alarm_actions', 'insufficient_data_actions', 'ok_actions'):
            action = (module.params.get(attr) or [])
            if (getattr(alarm, attr) != action):
                changed = True
                setattr(alarm, attr, module.params.get(attr))
        try:
            if changed:
                connection.create_alarm(alarm)
        except BotoServerError as e:
            module.fail_json(msg=str(e))
    result = alarms[0]
    module.exit_json(changed=changed, name=result.name, actions_enabled=result.actions_enabled, alarm_actions=result.alarm_actions, alarm_arn=result.alarm_arn, comparison=result.comparison, description=result.description, dimensions=result.dimensions, evaluation_periods=result.evaluation_periods, insufficient_data_actions=result.insufficient_data_actions, last_updated=result.last_updated, metric=result.metric, namespace=result.namespace, ok_actions=result.ok_actions, period=result.period, state_reason=result.state_reason, state_value=result.state_value, statistic=result.statistic, threshold=result.threshold, unit=result.unit)