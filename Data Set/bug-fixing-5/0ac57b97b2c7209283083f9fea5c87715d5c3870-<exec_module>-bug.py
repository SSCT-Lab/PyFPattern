def exec_module(self):
    changed = False
    result = dict()
    state = self.want.state
    try:
        if (state == 'present'):
            changed = self.present()
        elif (state == 'absent'):
            changed = self.absent()
    except iControlUnexpectedHTTPError as e:
        raise F5ModuleError(str(e))
    changes = self.changes.to_return()
    result.update(**changes)
    result.update(dict(changed=changed))
    return result