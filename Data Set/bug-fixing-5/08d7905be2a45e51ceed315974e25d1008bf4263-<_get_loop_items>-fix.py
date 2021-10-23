def _get_loop_items(self):
    '\n        Loads a lookup plugin to handle the with_* portion of a task (if specified),\n        and returns the items result.\n        '
    play_context_vars = dict()
    self._play_context.update_vars(play_context_vars)
    old_vars = dict()
    for k in play_context_vars:
        if (k in self._job_vars):
            old_vars[k] = self._job_vars[k]
        self._job_vars[k] = play_context_vars[k]
    self._job_vars['ansible_search_path'] = self._task.get_search_path()
    if (self._loader.get_basedir() not in self._job_vars['ansible_search_path']):
        self._job_vars['ansible_search_path'].append(self._loader.get_basedir())
    templar = Templar(loader=self._loader, shared_loader_obj=self._shared_loader_obj, variables=self._job_vars)
    items = None
    loop_cache = self._job_vars.get('_ansible_loop_cache')
    if (loop_cache is not None):
        items = loop_cache
    elif self._task.loop_with:
        if (self._task.loop_with in self._shared_loader_obj.lookup_loader):
            fail = True
            if (self._task.loop_with == 'first_found'):
                fail = False
            loop_terms = listify_lookup_plugin_terms(terms=self._task.loop, templar=templar, loader=self._loader, fail_on_undefined=fail, convert_bare=False)
            if (not fail):
                loop_terms = [t for t in loop_terms if (not templar.is_template(t))]
            mylookup = self._shared_loader_obj.lookup_loader.get(self._task.loop_with, loader=self._loader, templar=templar)
            for subdir in ['template', 'var', 'file']:
                if (subdir in self._task.action):
                    break
            setattr(mylookup, '_subdir', (subdir + 's'))
            items = mylookup.run(terms=loop_terms, variables=self._job_vars, wantlist=True)
        else:
            raise AnsibleError(("Unexpected failure in finding the lookup named '%s' in the available lookup plugins" % self._task.loop_with))
    elif (self._task.loop is not None):
        items = templar.template(self._task.loop)
        if (not isinstance(items, list)):
            raise AnsibleError(("Invalid data passed to 'loop', it requires a list, got this instead: %s. Hint: If you passed a list/dict of just one element, try adding wantlist=True to your lookup invocation or use q/query instead of lookup." % items))
    for k in play_context_vars:
        if (k in old_vars):
            self._job_vars[k] = old_vars[k]
        else:
            del self._job_vars[k]
    if items:
        for (idx, item) in enumerate(items):
            if ((item is not None) and (not isinstance(item, AnsibleUnsafe))):
                items[idx] = UnsafeProxy(item)
    return items