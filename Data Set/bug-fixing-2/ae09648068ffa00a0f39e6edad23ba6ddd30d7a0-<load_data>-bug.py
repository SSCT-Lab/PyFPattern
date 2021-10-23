

def load_data(self, ds, basedir, variable_manager=None, loader=None):
    "\n        Overrides the base load_data(), as we're actually going to return a new\n        Playbook() object rather than a PlaybookInclude object\n        "
    from ansible.playbook import Playbook
    new_obj = super(PlaybookInclude, self).load_data(ds, variable_manager, loader)
    all_vars = self.vars.copy()
    if variable_manager:
        all_vars.update(variable_manager.get_vars(loader=loader))
    templar = Templar(loader=loader, variables=all_vars)
    try:
        forward_conditional = False
        if (not new_obj.evaluate_conditional(templar=templar, all_vars=all_vars)):
            return None
    except AnsibleError:
        forward_conditional = True
    pb = Playbook(loader=loader)
    file_name = templar.template(new_obj.include)
    if (not os.path.isabs(file_name)):
        file_name = os.path.join(basedir, file_name)
    pb._load_playbook_data(file_name=file_name, variable_manager=variable_manager)
    for entry in pb._entries:
        temp_vars = entry.vars.copy()
        temp_vars.update(new_obj.vars)
        param_tags = temp_vars.pop('tags', None)
        if (param_tags is not None):
            entry.tags.extend(param_tags.split(','))
        entry.vars = temp_vars
        entry.tags = list(set(entry.tags).union(new_obj.tags))
        if (entry._included_path is None):
            entry._included_path = os.path.dirname(file_name)
        if forward_conditional:
            for task_block in entry.tasks:
                task_block.when = (self.when[:] + task_block.when)
    return pb
