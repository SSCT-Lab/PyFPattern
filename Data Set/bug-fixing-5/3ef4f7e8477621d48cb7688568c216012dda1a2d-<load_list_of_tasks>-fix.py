def load_list_of_tasks(ds, play, block=None, role=None, task_include=None, use_handlers=False, variable_manager=None, loader=None):
    '\n    Given a list of task datastructures (parsed from YAML),\n    return a list of Task() or TaskInclude() objects.\n    '
    from ansible.playbook.block import Block
    from ansible.playbook.handler import Handler
    from ansible.playbook.task import Task
    from ansible.playbook.task_include import TaskInclude
    from ansible.playbook.role_include import IncludeRole
    from ansible.playbook.handler_task_include import HandlerTaskInclude
    from ansible.template import Templar
    assert isinstance(ds, list), ('The ds (%s) should be a list but was a %s' % (ds, type(ds)))
    task_list = []
    for task_ds in ds:
        assert isinstance(task_ds, dict), ('The ds (%s) should be a dict but was a %s' % (ds, type(ds)))
        if ('block' in task_ds):
            t = Block.load(task_ds, play=play, parent_block=block, role=role, task_include=task_include, use_handlers=use_handlers, variable_manager=variable_manager, loader=loader)
            task_list.append(t)
        elif (('include' in task_ds) or ('import_tasks' in task_ds) or ('include_tasks' in task_ds)):
            if ('include' in task_ds):
                display.deprecated("The use of 'include' for tasks has been deprecated. Use 'import_tasks' for static inclusions or 'include_tasks' for dynamic inclusions")
            if use_handlers:
                include_class = HandlerTaskInclude
            else:
                include_class = TaskInclude
            t = include_class.load(task_ds, block=block, role=role, task_include=None, variable_manager=variable_manager, loader=loader)
            all_vars = variable_manager.get_vars(play=play, task=t)
            templar = Templar(loader=loader, variables=all_vars)
            if ('include_tasks' in task_ds):
                is_static = False
            elif ('import_tasks' in task_ds):
                is_static = True
            elif (t.static is not None):
                display.deprecated("The use of 'static' has been deprecated. Use 'import_tasks' for static inclusion, or 'include_tasks' for dynamic inclusion")
                is_static = t.static
            else:
                is_static = (C.DEFAULT_TASK_INCLUDES_STATIC or (use_handlers and C.DEFAULT_HANDLER_INCLUDES_STATIC) or ((not templar._contains_vars(t.args['_raw_params'])) and t.all_parents_static() and (not t.loop)))
            if is_static:
                if (t.loop is not None):
                    if ('import_tasks' in task_ds):
                        raise AnsibleParserError("You cannot use loops on 'import_tasks' statements. You should use 'include_tasks' instead.", obj=task_ds)
                    else:
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
                    parent_include_dir = os.path.dirname(templar.template(parent_include.args.get('_raw_params')))
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
                        raise AnsibleParserError(('Error when evaluating variable in include name: %s.\n\nWhen using static includes, ensure that any variables used in their names are defined in vars/vars_files\nor extra-vars passed in from the command line. Static includes cannot use variables from inventory\nsources like group or host vars.' % t.args['_raw_params']), obj=task_ds, suppress_extended_error=True, orig_exc=e)
                    if t._role:
                        include_file = loader.path_dwim_relative(t._role._role_path, subdir, include_target)
                    else:
                        include_file = loader.path_dwim(include_target)
                try:
                    data = loader.load_from_file(include_file)
                    if (data is None):
                        display.warning(('file %s is empty and had no tasks to include' % include_file))
                        continue
                    elif (not isinstance(data, list)):
                        raise AnsibleParserError('included task files must contain a list of tasks', obj=data)
                    display.vv(('statically imported: %s' % include_file))
                except AnsibleFileNotFound:
                    if (t.static or C.DEFAULT_TASK_INCLUDES_STATIC or (C.DEFAULT_HANDLER_INCLUDES_STATIC and use_handlers)):
                        raise
                    display.deprecated(("Included file '%s' not found, however since this include is not explicitly marked as 'static: yes', we will try and include it dynamically later. In the future, this will be an error unless 'static: no' is used on the include task. If you do not want missing includes to be considered dynamic, use 'static: yes' on the include or set the global ansible.cfg options to make all includes static for tasks and/or handlers" % include_file), version='2.7')
                    task_list.append(t)
                    continue
                ti_copy = t.copy(exclude_parent=True)
                ti_copy._parent = block
                included_blocks = load_list_of_blocks(data, play=play, parent_block=None, task_include=ti_copy, role=role, use_handlers=use_handlers, loader=loader, variable_manager=variable_manager)
                tags = ti_copy.vars.pop('tags', [])
                if isinstance(tags, string_types):
                    tags = tags.split(',')
                if (len(tags) > 0):
                    if (len(ti_copy.tags) > 0):
                        raise AnsibleParserError('Include tasks should not specify tags in more than one way (both via args and directly on the task). Mixing styles in which tags are specified is prohibited for whole import hierarchy, not only for single import statement', obj=task_ds, suppress_extended_error=True)
                    display.deprecated('You should not specify tags in the include parameters. All tags should be specified using the task-level option', version='2.7')
                else:
                    tags = ti_copy.tags[:]
                for b in included_blocks:
                    b.tags = list(set(b.tags).union(tags))
                if use_handlers:
                    for b in included_blocks:
                        task_list.extend(b.block)
                else:
                    task_list.extend(included_blocks)
            else:
                t.is_static = False
                task_list.append(t)
        elif (('include_role' in task_ds) or ('import_role' in task_ds)):
            ir = IncludeRole.load(task_ds, block=block, role=role, task_include=None, variable_manager=variable_manager, loader=loader)
            is_static = False
            if ('import_role' in task_ds):
                is_static = True
            elif (ir.static is not None):
                display.deprecated("The use of 'static' for 'include_role' has been deprecated. Use 'import_role' for static inclusion, or 'include_role' for dynamic inclusion")
                is_static = ir.static
            if is_static:
                if (ir.loop is not None):
                    if ('import_tasks' in task_ds):
                        raise AnsibleParserError("You cannot use loops on 'import_role' statements. You should use 'include_role' instead.", obj=task_ds)
                    else:
                        raise AnsibleParserError("You cannot use 'static' on an include_role with a loop", obj=task_ds)
                ir.statically_loaded = True
                all_vars = variable_manager.get_vars(play=play, task=ir)
                templar = Templar(loader=loader, variables=all_vars)
                if templar._contains_vars(ir._role_name):
                    ir._role_name = templar.template(ir._role_name)
                (blocks, _) = ir.get_block_list(variable_manager=variable_manager, loader=loader)
                t = task_list.extend(blocks)
            else:
                t = task_list.append(ir)
        else:
            if use_handlers:
                t = Handler.load(task_ds, block=block, role=role, task_include=task_include, variable_manager=variable_manager, loader=loader)
            else:
                t = Task.load(task_ds, block=block, role=role, task_include=task_include, variable_manager=variable_manager, loader=loader)
            task_list.append(t)
    return task_list