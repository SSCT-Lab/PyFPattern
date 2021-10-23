def act(self):
    '\n        Figure out what you want to do from ansible, and then do it.\n        '
    state_before = self.get_state_for(self.backend, self.host)
    self.command_results['state_before'] = state_before
    if (self.state == 'enabled'):
        self.enabled(self.host, self.backend, self.weight)
    elif ((self.state == 'disabled') and self._drain):
        self.drain(self.host, self.backend, status='MAINT')
    elif (self.state == 'disabled'):
        self.disabled(self.host, self.backend, self.shutdown_sessions)
    elif (self.state == 'drain'):
        self.drain(self.host, self.backend)
    else:
        self.module.fail_json(msg=("unknown state specified: '%s'" % self.state))
    state_after = self.get_state_for(self.backend, self.host)
    self.command_results['state_after'] = state_after
    if (state_before != state_after):
        self.command_results['changed'] = True
        self.module.exit_json(**self.command_results)
    else:
        self.command_results['changed'] = False
        self.module.exit_json(**self.command_results)