

def set_attributes_if_different(self, path, attributes, changed, diff=None, expand=True):
    if (attributes is None):
        return changed
    b_path = to_bytes(path, errors='surrogate_then_strict')
    if expand:
        b_path = os.path.expanduser(os.path.expandvars(b_path))
    path = to_text(b_path, errors='surrogate_then_strict')
    if (existing.get('attr_flags', '') != attributes):
        attrcmd = self.get_bin_path('chattr')
        if attrcmd:
            attrcmd = [attrcmd, ('=%s' % attributes), b_path]
            changed = True
            if (diff is not None):
                if ('before' not in diff):
                    diff['before'] = {
                        
                    }
                diff['before']['attributes'] = existing.get('attr_flags')
                if ('after' not in diff):
                    diff['after'] = {
                        
                    }
                diff['after']['attributes'] = attributes
            if (not self.check_mode):
                try:
                    (rc, out, err) = self.run_command(attrcmd)
                    if ((rc != 0) or err):
                        raise Exception(('Error while setting attributes: %s' % (out + err)))
                except:
                    e = get_exception()
                    self.fail_json(path=path, msg='chattr failed', details=str(e))
    return changed
