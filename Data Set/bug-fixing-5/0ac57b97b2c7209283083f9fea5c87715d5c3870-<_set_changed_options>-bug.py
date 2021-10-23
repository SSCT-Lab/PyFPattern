def _set_changed_options(self):
    changed = {
        
    }
    try:
        for key in Parameters.returnables:
            if (getattr(self.want, key) is not None):
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = Changes(params=changed)
    except Exception:
        pass