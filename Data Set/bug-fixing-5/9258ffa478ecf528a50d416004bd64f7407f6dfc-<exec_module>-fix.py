def exec_module(self, **kwargs):
    for key in (list(self.module_arg_spec.keys()) + ['tags']):
        setattr(self, key, kwargs[key])
    results = None
    changed = False
    self.log('Fetching auto scale settings {0}'.format(self.name))
    results = self.get_auto_scale()
    if (results and (self.state == 'absent')):
        changed = True
        if (not self.check_mode):
            self.delete_auto_scale()
    elif (self.state == 'present'):
        if (not self.location):
            resource_group = self.get_resource_group(self.resource_group)
            self.location = resource_group.location
        resource_id = self.target
        if isinstance(self.target, dict):
            resource_id = format_resource_id(val=self.target['name'], subscription_id=(self.target.get('subscription_id') or self.subscription_id), namespace=self.target['namespace'], types=self.target['types'], resource_group=(self.target.get('resource_group') or self.resource_group))
        self.target = resource_id
        resource_name = self.name

        def create_rule_instance(params):
            rule = params.copy()
            rule['metric_resource_uri'] = rule.get('metric_resource_uri', self.target)
            rule['time_grain'] = timedelta(minutes=rule.get('time_grain', 0))
            rule['time_window'] = timedelta(minutes=rule.get('time_window', 0))
            rule['cooldown'] = timedelta(minutes=rule.get('cooldown', 0))
            return ScaleRule(metric_trigger=MetricTrigger(**rule), scale_action=ScaleAction(**rule))
        profiles = [AutoscaleProfile(name=p.get('name'), capacity=ScaleCapacity(minimum=p.get('min_count'), maximum=p.get('max_count'), default=p.get('count')), rules=[create_rule_instance(r) for r in (p.get('rules') or [])], fixed_date=(TimeWindow(time_zone=p.get('fixed_date_timezone'), start=p.get('fixed_date_start'), end=p.get('fixed_date_end')) if p.get('fixed_date_timezone') else None), recurrence=(Recurrence(frequency=p.get('recurrence_frequency'), schedule=RecurrentSchedule(time_zone=p.get('recurrence_timezone'), days=p.get('recurrence_days'), hours=p.get('recurrence_hours'), minutes=p.get('recurrence_mins'))) if (p.get('recurrence_frequency') and (p['recurrence_frequency'] != 'None')) else None)) for p in (self.profiles or [])]
        notifications = [AutoscaleNotification(email=EmailNotification(**n), webhooks=[WebhookNotification(service_uri=w) for w in (n.get('webhooks') or [])]) for n in (self.notifications or [])]
        if (not results):
            changed = True
        else:
            resource_name = (results.autoscale_setting_resource_name or self.name)
            (update_tags, tags) = self.update_tags(results.tags)
            if update_tags:
                changed = True
                self.tags = tags
            if (self.target != results.target_resource_uri):
                changed = True
            if (self.enabled != results.enabled):
                changed = True
            profile_result_set = set([str(profile_to_dict(p)) for p in (results.profiles or [])])
            if (profile_result_set != set([str(profile_to_dict(p)) for p in profiles])):
                changed = True
            notification_result_set = set([str(notification_to_dict(n)) for n in (results.notifications or [])])
            if (notification_result_set != set([str(notification_to_dict(n)) for n in notifications])):
                changed = True
        if changed:
            results = AutoscaleSettingResource(location=self.location, tags=self.tags, profiles=profiles, notifications=notifications, enabled=self.enabled, autoscale_setting_resource_name=resource_name, target_resource_uri=self.target)
            if (not self.check_mode):
                results = self.create_or_update_auto_scale(results)
    self.results = auto_scale_to_dict(results)
    self.results['changed'] = changed
    return self.results