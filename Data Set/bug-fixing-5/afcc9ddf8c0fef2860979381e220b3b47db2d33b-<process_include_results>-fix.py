@staticmethod
def process_include_results(results, iterator, loader, variable_manager):
    included_files = []
    task_vars_cache = {
        
    }
    for res in results:
        original_host = res._host
        original_task = res._task
        if (original_task.action in ('include', 'include_tasks', 'include_role')):
            if original_task.loop:
                if ('results' not in res._result):
                    continue
                include_results = res._result['results']
            else:
                include_results = [res._result]
            for include_result in include_results:
                if ((('skipped' in include_result) and include_result['skipped']) or (('failed' in include_result) and include_result['failed'])):
                    continue
                cache_key = (iterator._play, original_host, original_task)
                try:
                    task_vars = task_vars_cache[cache_key]
                except KeyError:
                    task_vars = task_vars_cache[cache_key] = variable_manager.get_vars(play=iterator._play, host=original_host, task=original_task)
                templar = Templar(loader=loader, variables=task_vars)
                include_variables = include_result.get('include_variables', dict())
                loop_var = 'item'
                index_var = None
                if original_task.loop_control:
                    loop_var = original_task.loop_control.loop_var
                    index_var = original_task.loop_control.index_var
                if (loop_var in include_result):
                    task_vars[loop_var] = include_variables[loop_var] = include_result[loop_var]
                if (index_var and (index_var in include_result)):
                    task_vars[index_var] = include_variables[index_var] = include_result[index_var]
                if (original_task.action in ('include', 'include_tasks')):
                    include_file = None
                    if original_task:
                        if original_task.static:
                            continue
                        if original_task._parent:
                            parent_include = original_task._parent
                            cumulative_path = None
                            while (parent_include is not None):
                                if (not isinstance(parent_include, TaskInclude)):
                                    parent_include = parent_include._parent
                                    continue
                                if isinstance(parent_include, IncludeRole):
                                    parent_include_dir = parent_include._role_path
                                else:
                                    parent_include_dir = os.path.dirname(templar.template(parent_include.args.get('_raw_params')))
                                if ((cumulative_path is not None) and (not os.path.isabs(cumulative_path))):
                                    cumulative_path = os.path.join(parent_include_dir, cumulative_path)
                                else:
                                    cumulative_path = parent_include_dir
                                include_target = templar.template(include_result['include'])
                                if original_task._role:
                                    new_basedir = os.path.join(original_task._role._role_path, 'tasks', cumulative_path)
                                    candidates = [loader.path_dwim_relative(original_task._role._role_path, 'tasks', include_target), loader.path_dwim_relative(new_basedir, 'tasks', include_target)]
                                    for include_file in candidates:
                                        try:
                                            os.stat(include_file)
                                            break
                                        except OSError:
                                            pass
                                else:
                                    include_file = loader.path_dwim_relative(loader.get_basedir(), cumulative_path, include_target)
                                if os.path.exists(include_file):
                                    break
                                else:
                                    parent_include = parent_include._parent
                    if (include_file is None):
                        if original_task._role:
                            include_target = templar.template(include_result['include'])
                            include_file = loader.path_dwim_relative(original_task._role._role_path, 'tasks', include_target)
                        else:
                            include_file = loader.path_dwim(include_result['include'])
                    include_file = templar.template(include_file)
                    inc_file = IncludedFile(include_file, include_variables, original_task)
                else:
                    role_name = include_variables.get('name', include_variables.get('role', None))
                    if (role_name is not None):
                        role_name = templar.template(role_name)
                    new_task = original_task.copy()
                    new_task._role_name = role_name
                    for from_arg in new_task.FROM_ARGS:
                        if (from_arg in include_variables):
                            from_key = from_arg.replace('_from', '')
                            new_task._from_files[from_key] = templar.template(include_variables[from_arg])
                    inc_file = IncludedFile('role', include_variables, new_task, is_role=True)
                try:
                    pos = included_files.index(inc_file)
                    inc_file = included_files[pos]
                except ValueError:
                    included_files.append(inc_file)
                inc_file.add_host(original_host)
    return included_files