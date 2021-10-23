@enable_mode
def edit_config(self, candidate, check_mode=False, replace=None):
    if (not candidate):
        raise ValueError('must provide a candidate config to load')
    if (check_mode not in (True, False)):
        raise ValueError(('`check_mode` must be a bool, got %s' % check_mode))
    device_operations = self.get_device_operations()
    options = self.get_options()
    if (replace and (replace not in options['replace'])):
        raise ValueError(('`replace` value %s in invalid, valid values are %s' % (replace, options['replace'])))
    results = []
    if (not check_mode):
        for line in chain(['configure terminal'], to_list(candidate)):
            if ((line != 'end') and (line[0] != '!')):
                if (not isinstance(line, collections.Mapping)):
                    line = {
                        'command': line,
                    }
            results.append(self.send_command(**line))
        results.append(self.send_command('end'))
    return results[1:(- 1)]