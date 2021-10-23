

def preprocess_data(self, ds):
    '\n        tasks are especially complex arguments so need pre-processing.\n        keep it short.\n        '
    assert isinstance(ds, dict), ('ds (%s) should be a dict but was a %s' % (ds, type(ds)))
    new_ds = AnsibleMapping()
    if isinstance(ds, AnsibleBaseYAMLObject):
        new_ds.ansible_pos = ds.ansible_pos
    args_parser = ModuleArgsParser(task_ds=ds)
    try:
        (action, args, delegate_to) = args_parser.parse()
    except AnsibleParserError as e:
        raise AnsibleParserError(to_native(e), obj=ds, orig_exc=e)
    if (action in ('command', 'shell', 'script')):
        if ('cmd' in args):
            if (args.get('_raw_params', '') != ''):
                raise AnsibleError("The 'cmd' argument cannot be used when other raw parameters are specified. Please put everything in one or the other place.", obj=ds)
            args['_raw_params'] = args.pop('cmd')
    new_ds['action'] = action
    new_ds['args'] = args
    new_ds['delegate_to'] = delegate_to
    if ('vars' in ds):
        new_ds['vars'] = self._load_vars(None, ds.get('vars'))
    else:
        new_ds['vars'] = dict()
    for (k, v) in iteritems(ds):
        if ((k in ('action', 'local_action', 'args', 'delegate_to')) or (k == action) or (k == 'shell')):
            continue
        elif (k.replace('with_', '') in lookup_loader):
            self._preprocess_loop(ds, new_ds, k, v)
        elif ((action in ('include', 'include_tasks')) and (k not in self._valid_attrs) and (k not in self.DEPRECATED_ATTRIBUTES)):
            display.deprecated('Specifying include variables at the top-level of the task is deprecated. Please see:\nhttp://docs.ansible.com/ansible/playbooks_roles.html#task-include-files-and-encouraging-reuse\n\n for currently supported syntax regarding included files and variables', version='2.7')
            new_ds['vars'][k] = v
        else:
            new_ds[k] = v
    return super(Task, self).preprocess_data(new_ds)
