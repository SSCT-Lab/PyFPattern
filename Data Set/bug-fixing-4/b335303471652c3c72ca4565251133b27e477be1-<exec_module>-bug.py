def exec_module(self, **kwargs):
    for key in (list(self.module_arg_spec.keys()) + ['tags']):
        setattr(self, key, kwargs[key])
    self.client = self.get_keyvault_client()
    results = dict()
    changed = False
    try:
        results['secret_id'] = self.get_secret(self.secret_name)
        if (self.state == 'absent'):
            changed = True
    except KeyVaultErrorException:
        if (self.state == 'present'):
            changed = True
    self.results['changed'] = changed
    self.results['state'] = results
    if (not self.check_mode):
        if ((self.state == 'present') and changed):
            results['secret_id'] = self.create_secret(self.secret_name, self.secret_value, self.tags)
            self.results['state'] = results
            self.results['state']['status'] = 'Created'
        elif ((self.state == 'absent') and changed):
            results['secret_id'] = self.delete_secret(self.secret_name)
            self.results['state'] = results
            self.results['state']['status'] = 'Deleted'
    elif ((self.state == 'present') and changed):
        self.results['state']['status'] = 'Created'
    elif ((self.state == 'absent') and changed):
        self.results['state']['status'] = 'Deleted'
    return self.results