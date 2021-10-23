def commit(self, comment=None, label=None, replace=None):
    cmd_obj = {
        
    }
    if replace:
        cmd_obj['command'] = 'commit replace'
        cmd_obj['prompt'] = 'This commit will replace or remove the entire running configuration'
        cmd_obj['answer'] = 'yes'
    else:
        if (comment and label):
            cmd_obj['command'] = 'commit label {0} comment {1}'.format(label, comment)
        elif comment:
            cmd_obj['command'] = 'commit comment {0}'.format(comment)
        elif label:
            cmd_obj['command'] = 'commit label {0}'.format(label)
        else:
            cmd_obj['command'] = 'commit show-error'
        cmd_obj['prompt'] = '(C|c)onfirm'
        cmd_obj['answer'] = 'y'
    self.send_command(**cmd_obj)