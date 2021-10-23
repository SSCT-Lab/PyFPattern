def parse(self):
    '\n        Given a task in one of the supported forms, parses and returns\n        returns the action, arguments, and delegate_to values for the\n        task, dealing with all sorts of levels of fuzziness.\n        '
    thing = None
    action = None
    delegate_to = self._task_ds.get('delegate_to', None)
    args = dict()
    additional_args = self._task_ds.get('args', dict())
    if ('action' in self._task_ds):
        thing = self._task_ds['action']
        (action, args) = self._normalize_parameters(thing, action=action, additional_args=additional_args)
    if ('local_action' in self._task_ds):
        if (action is not None):
            raise AnsibleParserError('action and local_action are mutually exclusive', obj=self._task_ds)
        thing = self._task_ds.get('local_action', '')
        delegate_to = 'localhost'
        (action, args) = self._normalize_parameters(thing, action=action, additional_args=additional_args)
    for (item, value) in iteritems(self._task_ds):
        if ((item in module_loader) or (item in action_loader) or (item in ['meta', 'include', 'include_tasks', 'include_role', 'import_tasks', 'import_role'])):
            if (action is not None):
                raise AnsibleParserError(('conflicting action statements: %s, %s' % (action, item)), obj=self._task_ds)
            action = item
            thing = value
            (action, args) = self._normalize_parameters(thing, action=action, additional_args=additional_args)
    if (action is None):
        if ('ping' not in module_loader):
            raise AnsibleParserError("The requested action was not found in configured module paths. Additionally, core modules are missing. If this is a checkout, run 'git pull --rebase' to correct this problem.", obj=self._task_ds)
        else:
            raise AnsibleParserError('no action detected in task. This often indicates a misspelled module name, or incorrect module path.', obj=self._task_ds)
    elif ((args.get('_raw_params', '') != '') and (action not in RAW_PARAM_MODULES)):
        templar = Templar(loader=None)
        raw_params = args.pop('_raw_params')
        if templar._contains_vars(raw_params):
            args['_variable_params'] = raw_params
        else:
            raise AnsibleParserError(("this task '%s' has extra params, which is only allowed in the following modules: %s" % (action, ', '.join(RAW_PARAM_MODULES))), obj=self._task_ds)
    return (action, args, delegate_to)