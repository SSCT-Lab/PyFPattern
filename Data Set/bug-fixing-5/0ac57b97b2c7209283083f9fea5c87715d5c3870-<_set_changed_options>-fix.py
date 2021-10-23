def _set_changed_options(self):
    changed = {
        
    }
    for key in Parameters.returnables:
        if (getattr(self.want, key) is not None):
            changed[key] = getattr(self.want, key)
    if changed:
        self.changes = UsableChanges(params=changed)