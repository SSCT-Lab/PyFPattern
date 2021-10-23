def work(self):
    'worker'
    self.check_params()
    self.get_proposed()
    if (self.action == 'rollback'):
        if self.commit_id:
            self.rollback_commit_id()
        if self.label:
            self.rollback_label()
        if self.filename:
            self.rollback_filename()
        if self.last:
            self.rollback_last()
    elif (self.action == 'set'):
        if (self.commit_id and self.label):
            self.set_commitid_label()
    elif (self.action == 'clear'):
        if self.commit_id:
            self.clear_commitid_label()
        if self.oldest:
            self.clear_oldest()
    elif (self.action == 'commit'):
        if self.label:
            self.commit_label()
    elif (self.action == 'display'):
        self.rollback_info = self.get_rollback_dict()
    self.get_existing()
    self.get_end_state()
    self.results['changed'] = self.changed
    self.results['proposed'] = self.proposed
    self.results['existing'] = self.existing
    self.results['end_state'] = self.end_state
    if self.changed:
        self.results['updates'] = self.updates_cmd
    else:
        self.results['updates'] = list()
    self.module.exit_json(**self.results)