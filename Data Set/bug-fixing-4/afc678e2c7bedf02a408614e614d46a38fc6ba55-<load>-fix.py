@staticmethod
def load(data, variable_manager=None, loader=None, vars=None):
    if ((('name' not in data) or (data['name'] is None)) and ('hosts' in data)):
        if ((data['hosts'] is None) or all(((host is None) for host in data['hosts']))):
            raise AnsibleParserError('Hosts list cannot be empty - please check your playbook')
        if isinstance(data['hosts'], list):
            data['name'] = ','.join(data['hosts'])
        else:
            data['name'] = data['hosts']
    p = Play()
    if vars:
        p.vars = vars.copy()
    return p.load_data(data, variable_manager=variable_manager, loader=loader)