

def _mangle_fields(self, fields, uri, filter_patterns=None):
    filter_patterns = (['public-keys-0'] if (filter_patterns is None) else filter_patterns)
    new_fields = {
        
    }
    for (key, value) in fields.items():
        split_fields = key[len(uri):].split('/')
        if ((len(split_fields) == 3) and (split_fields[0:2] == ['iam', 'security-credentials']) and ('_' not in split_fields[2])):
            new_fields[(self._prefix % 'iam-instance-profile-role')] = split_fields[2]
        if ((len(split_fields) > 1) and split_fields[1]):
            new_key = '-'.join(split_fields)
            new_fields[(self._prefix % new_key)] = value
        else:
            new_key = ''.join(split_fields)
            new_fields[(self._prefix % new_key)] = value
    for pattern in filter_patterns:
        for key in dict(new_fields):
            match = re.search(pattern, key)
            if match:
                new_fields.pop(key)
    return new_fields
