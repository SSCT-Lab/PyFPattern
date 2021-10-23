def load_list_of_tasks(ds, play, block=None, role=None, task_include=None, use_handlers=False, variable_manager=None, loader=None):
    '\n    Given a list of task datastructures (parsed from YAML),\n    return a list of Task() or TaskInclude() objects.\n    '
    from ansible.playbook.block import Block
    from ansible.playbook.handler import Handler
    from ansible.playbook.task import Task
    from ansible.playbook.task_include import TaskInclude
    from ansible.playbook.handler_task_include import HandlerTaskInclude
    from ansible.template import Templar
    assert isinstance(ds, list)
    task_list = []
    for task_ds in ds:
        assert isinstance(task_ds, dict)
        if ('block' in task_ds):
            t = Block.load(task_ds, play=play, parent_block=block, role=role, task_include=task_include, use_handlers=use_handlers, variable_manager=variable_manager, loader=loader)
            task_list.append(t)
        elif ('include' in task_ds):
            if use_handlers:
                include_class = HandlerTaskInclude
            else:
                include_class = TaskInclude
            t = include_class.load(task_ds, block=block, role=role, task_include=None, variable_manager=variable_manager, loader=loader)
            all_vars = variable_manager.get_vars(loader=loader, play=play, task=t)
            templar = Templar(loader=loader, variables=all_vars)
            if (t.static is not None):
                is_static = t.static
            else:
                is_static = (C.DEFAULT_TASK_INCLUDES_STATIC or (use_handlers and C.DEFAULT_HANDLER_INCLUDES_STATIC) or ((not templar._contains_vars(t.args['_raw_params'])) and t.all_parents_static() and (not t.loop)))
            if is_static:
                if (t.loop is not None):
                    raise AnsibleParserError("You cannot use 'static' on an include with a loop", obj=task_ds)
                t.statically_loaded = True
                parent_include = block
                cumulative_path = None
                found = False
                subdir = 'tasks'
                if use_handlers:
                    subdir = 'handlers'
                while (parent_include is not None):
                    if (not isinstance(parent_include, TaskInclude)):
                        parent_include = parent_include._parent
                        continue
                    parent_include_dir = templar.template(os.path.dirname(parent_include.args.get('_raw_params')))
                    if (cumulative_path is None):
                        cumulative_path = parent_include_dir
                    elif (not os.path.isabs(cumulative_path)):
                        cumulative_path = os.path.join(parent_include_dir, cumulative_path)
                    include_target = templar.template(t.args['_raw_params'])
                    if t._role:
                        new_basedir = os.path.join(t._role._role_path, subdir, cumulative_path)
                        include_file = loader.path_dwim_relative(new_basedir, subdir, include_target)
                    else:
                        include_file = loader.path_dwim_relative(loader.get_basedir(), cumulative_path, include_target)
                    if os.path.exists(include_file):
                        found = True
                        break
                    else:
                        parent_include = parent_include._parent
                if (not found):
                    try:
                        include_target = templar.template(t.args['_raw_params'])
                    except AnsibleUndefinedVariable as e:
                        raise AnsibleParserError(('Error when evaluating variable in include name: %s.\n\nWhen using static includes, ensure that any variables used in their names are defined in vars/vars_files\nor extra-vars passed in from the command line. Static includes cannot use variables from inventory\nsources like group or host vars.' % t.args['_raw_params']), obj=task_ds, suppress_extended_error=True)
                    if t._role:
                        include_file = loader.path_dwim_relative(t._role._role_path, subdir, include_target)
                    else:
                        include_file = loader.path_dwim(include_target)
                try:
                    data = loader.load_from_file(include_file)
                    if (data is None):
                        return []
                    elif (not isinstance(data, list)):
                        raise AnsibleParserError('included task files must contain a list of tasks', obj=data)
                    display.display(('statically included: %s' % include_file), color=C.COLOR_SKIP)
                except AnsibleFileNotFound as e:
                    if (t.static or C.DEFAULT_TASK_INCLUDES_STATIC or (C.DEFAULT_HANDLER_INCLUDES_STATIC and use_handlers)):
                        raise
                    display.deprecated(("Included file '%s' not found, however since this include is not explicitly marked as 'static: yes', we will try and include it dynamically later. In the future, this will be an error unless 'static: no' is used on the include task. If you do not want missing includes to be considered dynamic, use 'static: yes' on the include or set the global ansible.cfg options to make all inclues static for tasks and/or handlers" % include_file))
                    task_list.append(t)
                    continue
                included_blocks = load_list_of_blocks(data, play=play, parent_block=None, task_include=t.copy(), role=role, use_handlers=use_handlers, loader=loader, variable_manager=variable_manager)
                tags = t.vars.pop('tags', [])
                if isinstance(tags, string_types):
                    tags = tags.split(',')
                if (len(tags) > 0):
                    if (len(t.tags) > 0):
                        raise AnsibleParserError('Include tasks should not specify tags in more than one way (both via args and directly on the task). Mixing styles in which tags are specified is prohibited for whole import hierarchy, not only for single import statement', obj=task_ds, suppress_extended_error=True)
                    display.deprecated('You should not specify tags in the include parameters. All tags should be specified using the task-level option')
                else:
                    tags = t.tags[:]
                for b in included_blocks:
                    b.tags = list(set(b.tags).union(tags))
                if use_handlers:
                    for b in included_blocks:
                        task_list.extend(b.block)
                else:
                    task_list.extend(included_blocks)
            else:
                task_list.append(t)
        else:
            if use_handlers:
                t = Handler.load(task_ds, block=block, role=role, task_include=task_include, variable_manager=variable_manager, loader=loader)
            else:
                t = Task.load(task_ds, block=block, role=role, task_include=task_include, variable_manager=variable_manager, loader=loader)
            task_list.append(t)
    return task_list