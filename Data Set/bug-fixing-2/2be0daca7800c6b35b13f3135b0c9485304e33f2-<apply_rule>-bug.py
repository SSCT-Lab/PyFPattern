

def apply_rule(self, rule):
    match = (rule.data.get('action_match') or Rule.DEFAULT_ACTION_MATCH)
    condition_list = rule.data.get('conditions', ())
    frequency = (rule.data.get('frequency') or Rule.DEFAULT_FREQUENCY)
    if (not condition_list):
        return
    if ((rule.environment_id is not None) and (self.event.get_environment().id != rule.environment_id)):
        return
    status = self.get_rule_status(rule)
    now = timezone.now()
    freq_offset = (now - timedelta(minutes=frequency))
    if (status.last_active and (status.last_active > freq_offset)):
        return
    state = self.get_state()
    condition_iter = (self.condition_matches(c, state, rule) for c in condition_list)
    if (match == 'all'):
        passed = all(condition_iter)
    elif (match == 'any'):
        passed = any(condition_iter)
    elif (match == 'none'):
        passed = (not any(condition_iter))
    else:
        self.logger.error('Unsupported action_match %r for rule %d', match, rule.id)
        return
    if passed:
        passed = GroupRuleStatus.objects.filter(id=status.id).exclude(last_active__gt=freq_offset).update(last_active=now)
    if (not passed):
        return
    for action in rule.data.get('actions', ()):
        action_cls = rules.get(action['id'])
        if (action_cls is None):
            self.logger.warn('Unregistered action %r', action['id'])
            continue
        action_inst = action_cls(self.project, data=action, rule=rule)
        results = safe_execute(action_inst.after, event=self.event, state=state, _with_transaction=False)
        if (results is None):
            self.logger.warn('Action %s did not return any futures', action['id'])
            continue
        for future in results:
            key = ((future.key is not None) or future.callback)
            rule_future = RuleFuture(rule=rule, kwargs=future.kwargs)
            if (key not in self.grouped_futures):
                self.grouped_futures[key] = (future.callback, [rule_future])
            else:
                self.grouped_futures[key][1].append(rule_future)
