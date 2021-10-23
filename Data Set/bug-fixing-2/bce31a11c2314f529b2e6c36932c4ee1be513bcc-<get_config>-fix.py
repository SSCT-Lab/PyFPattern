

def get_config(self, include=None):
    if (include not in [None, 'defaults', 'passwords']):
        raise ValueError('include must be one of None, defaults, passwords')
    cmd = 'show running-config'
    if (include == 'passwords'):
        cmd = 'more system:running-config'
    elif (include == 'defaults'):
        cmd = 'show running-config all'
    else:
        cmd = 'show running-config'
    return self.run_commands(cmd)[0]
