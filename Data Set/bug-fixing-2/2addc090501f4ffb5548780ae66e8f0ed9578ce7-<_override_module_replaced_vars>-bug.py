

def _override_module_replaced_vars(self, task_vars):
    ' Some vars are substituted into the modules.  Have to make sure\n        that those are correct for localhost when synchronize creates its own\n        connection to localhost.'
    if ('ansible_syslog_facility' in task_vars):
        del task_vars['ansible_syslog_facility']
    for key in task_vars.keys():
        if (key.startswith('ansible_') and key.endswith('_interpreter')):
            del task_vars[key]
    for host in C.LOCALHOST:
        if (host in task_vars['hostvars']):
            localhost = task_vars['hostvars'][host]
            break
    if ('ansible_syslog_facility' in localhost):
        task_vars['ansible_syslog_facility'] = localhost['ansible_syslog_facility']
    for key in localhost:
        if (key.startswith('ansible_') and key.endswith('_interpreter')):
            task_vars[key] = localhost[key]
