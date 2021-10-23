def exec_module(self, **kwargs):
    self.network_client.config.long_running_operation_timeout = 3
    self.nsg_models = self.network_client.network_security_groups.models
    for key in (list(self.module_arg_spec.keys()) + ['tags']):
        setattr(self, key, kwargs[key])
    changed = False
    results = dict()
    resource_group = self.get_resource_group(self.resource_group)
    if (not self.location):
        self.location = resource_group.location
    if self.rules:
        for rule in self.rules:
            try:
                validate_rule(self, rule)
            except Exception as exc:
                self.fail('Error validating rule {0} - {1}'.format(rule, str(exc)))
    if self.default_rules:
        for rule in self.default_rules:
            try:
                validate_rule(self, rule, 'default')
            except Exception as exc:
                self.fail('Error validating default rule {0} - {1}'.format(rule, str(exc)))
    try:
        nsg = self.network_client.network_security_groups.get(self.resource_group, self.name)
        results = create_network_security_group_dict(nsg)
        self.log('Found security group:')
        self.log(results, pretty_print=True)
        self.check_provisioning_state(nsg, self.state)
        if (self.state == 'present'):
            pass
        elif (self.state == 'absent'):
            self.log("CHANGED: security group found but state is 'absent'")
            changed = True
    except CloudError:
        if (self.state == 'present'):
            self.log("CHANGED: security group not found and state is 'present'")
            changed = True
    if ((self.state == 'present') and (not changed)):
        self.log('Update security group {0}'.format(self.name))
        (update_tags, results['tags']) = self.update_tags(results['tags'])
        if update_tags:
            changed = True
        (rule_changed, new_rule) = compare_rules_change(results['rules'], self.rules, self.purge_rules)
        if rule_changed:
            changed = True
            results['rules'] = new_rule
        (rule_changed, new_rule) = compare_rules_change(results['default_rules'], self.default_rules, self.purge_default_rules)
        if rule_changed:
            changed = True
            results['default_rules'] = new_rule
        self.results['changed'] = changed
        self.results['state'] = results
        if ((not self.check_mode) and changed):
            self.results['state'] = self.create_or_update(results)
    elif ((self.state == 'present') and changed):
        self.log('Create security group {0}'.format(self.name))
        if (not self.location):
            self.fail('Parameter error: location required when creating a security group.')
        results['name'] = self.name
        results['location'] = self.location
        results['rules'] = []
        results['default_rules'] = []
        results['tags'] = {
            
        }
        if self.rules:
            results['rules'] = self.rules
        if self.default_rules:
            results['default_rules'] = self.default_rules
        if self.tags:
            results['tags'] = self.tags
        self.results['changed'] = changed
        self.results['state'] = results
        if (not self.check_mode):
            self.results['state'] = self.create_or_update(results)
    elif ((self.state == 'absent') and changed):
        self.log('Delete security group {0}'.format(self.name))
        self.results['changed'] = changed
        self.results['state'] = dict()
        if (not self.check_mode):
            self.delete()
            self.results['state']['status'] = 'Deleted'
    return self.results