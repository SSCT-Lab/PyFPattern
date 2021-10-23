def has_changed(self, want_dict, current_dict, only_keys=None):
    for (key, value) in want_dict.iteritems():
        if (only_keys and (key not in only_keys)):
            continue
        if (value is None):
            continue
        if (key in current_dict):
            if isinstance(value, (int, float, long, complex)):
                if isinstance(value, int):
                    current_dict[key] = int(current_dict[key])
                elif isinstance(value, float):
                    current_dict[key] = float(current_dict[key])
                elif isinstance(value, long):
                    current_dict[key] = long(current_dict[key])
                elif isinstance(value, complex):
                    current_dict[key] = complex(current_dict[key])
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