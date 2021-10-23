

def run(self, tmp=None, task_vars=None):
    ' handler for package operations '
    if (task_vars is None):
        task_vars = dict()
    result = super(ActionModule, self).run(tmp, task_vars)
    module = self._task.args.get('use', 'auto').lower()
    if (module == 'auto'):
        try:
            module = self._templar.template('{{ansible_service_mgr}}')
        except:
            pass
    if (module == 'auto'):
        facts = self._execute_module(module_name='setup', module_args=dict(gather_subset='!all', filter='ansible_service_mgr'), task_vars=task_vars)
        self._display.debug(('Facts %s' % facts))
        if (('ansible_facts' in facts) and ('ansible_service_mgr' in facts['ansible_facts'])):
            module = facts['ansible_facts']['ansible_service_mgr']
    if ((not module) or (module == 'auto') or (module not in self._shared_loader_obj.module_loader)):
        module = 'service'
    if (module != 'auto'):
        new_module_args = self._task.args.copy()
        if ('use' in new_module_args):
            del new_module_args['use']
        if (('state' in new_module_args) and (new_module_args['state'] == 'running')):
            new_module_args['state'] = 'started'
        self._display.vvvv(('Running %s' % module))
        result.update(self._execute_module(module_name=module, module_args=new_module_args, task_vars=task_vars))
    else:
        result['failed'] = True
        result['msg'] = 'Could not detect which service manager to use. Try gathering facts or setting the "use" option.'
    return result
