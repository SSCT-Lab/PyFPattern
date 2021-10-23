

def has_changed(self, want_dict, current_dict, only_keys=None):
    for (key, value) in want_dict.iteritems():
        if (only_keys and (key not in only_keys)):
            continue
        if (value is None):
            continue
        if (key in current_dict):
            if isinstance(current_dict[key], (int, long, float, complex)):
                if (value != current_dict[key]):
                    return True
            elif (self.case_sensitive_keys and (key in self.case_sensitive_keys)):
                if (value != current_dict[key].encode('utf-8')):
                    return True
            elif (value.lower() != current_dict[key].encode('utf-8').lower()):
                return True
        else:
            return True
    return False
