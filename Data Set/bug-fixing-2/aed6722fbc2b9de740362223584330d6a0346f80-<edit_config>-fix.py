

def edit_config(self, candidate=None, commit=True, admin=False, replace=None, comment=None, label=None):
    operations = self.get_device_operations()
    self.check_edit_config_capability(operations, candidate, commit, replace, comment)
    resp = {
        
    }
    results = []
    requests = []
    self.configure(admin=admin)
    if replace:
        candidate = 'load {0}'.format(replace)
    for line in to_list(candidate):
        if (not isinstance(line, collections.Mapping)):
            line = {
                'command': line,
            }
        cmd = line['command']
        results.append(self.send_command(**line))
        requests.append(cmd)
    if commit:
        self.commit(comment=comment, label=label, replace=replace)
    else:
        self.discard_changes()
    self.abort(admin=admin)
    resp['request'] = requests
    resp['response'] = results
    return resp
