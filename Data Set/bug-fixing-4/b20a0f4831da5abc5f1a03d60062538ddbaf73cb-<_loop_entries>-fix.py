def _loop_entries(self, container, entry_list):
    ' repeat code for value entry assignment '
    value = None
    origin = None
    for entry in entry_list:
        name = entry.get('name')
        try:
            temp_value = container.get(name, None)
        except UnicodeEncodeError:
            self.WARNINGS.add('value for config entry {0} contains invalid characters, ignoring...'.format(to_text(name)))
            continue
        if (temp_value is not None):
            value = temp_value
            origin = name
            if ('deprecated' in entry):
                self.DEPRECATED.append((entry['name'], entry['deprecated']))
    return (value, origin)