def _update_changed_options(self):
    changed = {
        
    }
    try:
        for key in Parameters.updatables:
            if (getattr(self.want, key) is not None):
                attr1 = getattr(self.want, key)
                attr2 = getattr(self.have, key)
                if (attr1 != attr2):
                    changed[key] = attr1
            if (self.want.key_checksum != self.have.checksum):
                changed['key_checksum'] = self.want.key_checksum
        if changed:
            self.changes = Changes(params=changed)
            return True
    except Exception:
        pass
    return False