def _update_changed_options(self):
    diff = Difference(self.want, self.have)
    updatables = Parameters.updatables
    changed = dict()
    for k in updatables:
        change = diff.compare(k)
        if (change is None):
            continue
        elif isinstance(change, dict):
            changed.update(change)
        else:
            changed[k] = change
    if changed:
        self.changes = UsableChanges(params=changed)
        return True
    return False