def exec_module(self):
    changed = False
    result = dict()
    state = self.want.state
    if (state == 'present'):
        changed = self.present()
    elif (state == 'absent'):
        changed = self.absent()
    reportable = ReportableChanges(params=self.changes.to_return())
    changes = reportable.to_return()
    result.update(**changes)
    result.update(dict(changed=changed))
    self._announce_deprecations(result)
    return result