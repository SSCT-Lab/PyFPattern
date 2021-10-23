

def run(self, iterator, play_context):
    '\n        The linear strategy is simple - get the next task and queue\n        it for all hosts, then wait for the queue to drain before\n        moving on to the next task\n        '
    result = self._tqm.RUN_OK
    work_to_do = True
    while (work_to_do and (not self._tqm._terminated)):
        try:
            display.debug('getting the remaining hosts for this loop')
            hosts_left = [host for host in self._inventory.get_hosts(iterator._play.hosts) if (host.name not in self._tqm._unreachable_hosts)]
            display.debug('done getting the remaining hosts for this loop')
            callback_sent = False
            work_to_do = False
            host_results = []
            host_tasks = self._get_next_task_lockstep(hosts_left, iterator)
            skip_rest = False
            choose_step = True
            any_errors_fatal = False
            results = []
            for (host, task) in host_tasks:
                if (not task):
                    continue
                if self._tqm._terminated:
                    break
                run_once = False
                work_to_do = True
                try:
                    action = action_loader.get(task.action, class_only=True)
                except KeyError:
                    action = None
                if (task._role and task._role.has_run(host)):
                    if ((task._role._metadata is None) or (task._role._metadata and (not task._role._metadata.allow_duplicates))):
                        display.debug(("'%s' skipped because role has already run" % task))
                        continue
                if (task.action == 'meta'):
                    results.extend(self._execute_meta(task, play_context, iterator))
                    if (task.args.get('_raw_params', None) != 'noop'):
                        run_once = True
                else:
                    if (self._step and choose_step):
                        if self._take_step(task):
                            choose_step = False
                        else:
                            skip_rest = True
                            break
                    display.debug('getting variables')
                    task_vars = self._variable_manager.get_vars(loader=self._loader, play=iterator._play, host=host, task=task)
                    self.add_tqm_variables(task_vars, play=iterator._play)
                    templar = Templar(loader=self._loader, variables=task_vars)
                    display.debug('done getting variables')
                    run_once = (templar.template(task.run_once) or (action and getattr(action, 'BYPASS_HOST_LOOP', False)))
                    if ((task.any_errors_fatal or run_once) and (not task.ignore_errors)):
                        any_errors_fatal = True
                    if (not callback_sent):
                        display.debug('sending task start callback, copying the task so we can template it temporarily')
                        saved_name = task.name
                        display.debug('done copying, going to template now')
                        try:
                            task.name = to_text(templar.template(task.name, fail_on_undefined=False), nonstring='empty')
                            display.debug('done templating')
                        except:
                            display.debug('templating failed for some reason')
                            pass
                        display.debug('here goes the callback...')
                        self._tqm.send_callback('v2_playbook_on_task_start', task, is_conditional=False)
                        task.name = saved_name
                        callback_sent = True
                        display.debug('sending task start callback')
                    self._blocked_hosts[host.get_name()] = True
                    self._queue_task(host, task, task_vars, play_context)
                    del task_vars
                if run_once:
                    break
                results += self._process_pending_results(iterator, max_passes=max(1, int((len(self._tqm._workers) * 0.1))))
            if skip_rest:
                continue
            display.debug('done queuing things up, now waiting for results queue to drain')
            if (self._pending_results > 0):
                results += self._wait_on_pending_results(iterator)
            host_results.extend(results)
            all_role_blocks = []
            for hr in results:
                if (hr._task.action == 'include_role'):
                    loop_var = None
                    if hr._task.loop:
                        loop_var = 'item'
                        if hr._task.loop_control:
                            loop_var = (hr._task.loop_control.loop_var or 'item')
                        include_results = hr._result['results']
                    else:
                        include_results = [hr._result]
                    for include_result in include_results:
                        if ((('skipped' in include_result) and include_result['skipped']) or (('failed' in include_result) and include_result['failed'])):
                            continue
                        display.debug('generating all_blocks data for role')
                        new_ir = hr._task.copy()
                        new_ir.vars.update(include_result.get('include_variables', dict()))
                        if (loop_var and (loop_var in include_result)):
                            new_ir.vars[loop_var] = include_result[loop_var]
                        all_role_blocks.extend(new_ir.get_block_list(play=iterator._play, variable_manager=self._variable_manager, loader=self._loader))
            if (len(all_role_blocks) > 0):
                for host in hosts_left:
                    iterator.add_tasks(host, all_role_blocks)
            try:
                included_files = IncludedFile.process_include_results(host_results, self._tqm, iterator=iterator, inventory=self._inventory, loader=self._loader, variable_manager=self._variable_manager)
            except AnsibleError as e:
                return self._tqm.RUN_ERROR
            include_failure = False
            if (len(included_files) > 0):
                display.debug('we have included files to process')
                noop_task = Task()
                noop_task.action = 'meta'
                noop_task.args['_raw_params'] = 'noop'
                noop_task.set_loader(iterator._play._loader)
                display.debug('generating all_blocks data')
                all_blocks = dict(((host, []) for host in hosts_left))
                display.debug('done generating all_blocks data')
                for included_file in included_files:
                    display.debug(('processing included file: %s' % included_file._filename))
                    try:
                        new_blocks = self._load_included_file(included_file, iterator=iterator)
                        display.debug('iterating over new_blocks loaded from include file')
                        for new_block in new_blocks:
                            task_vars = self._variable_manager.get_vars(loader=self._loader, play=iterator._play, task=included_file._task)
                            display.debug('filtering new block on tags')
                            final_block = new_block.filter_tagged_tasks(play_context, task_vars)
                            display.debug('done filtering new block on tags')
                            noop_block = Block(parent_block=task._parent)
                            noop_block.block = [noop_task for t in new_block.block]
                            noop_block.always = [noop_task for t in new_block.always]
                            noop_block.rescue = [noop_task for t in new_block.rescue]
                            for host in hosts_left:
                                if (host in included_file._hosts):
                                    all_blocks[host].append(final_block)
                                else:
                                    all_blocks[host].append(noop_block)
                        display.debug('done iterating over new_blocks loaded from include file')
                    except AnsibleError as e:
                        for host in included_file._hosts:
                            self._tqm._failed_hosts[host.name] = True
                            iterator.mark_host_failed(host)
                        display.error(to_text(e), wrap_text=False)
                        include_failure = True
                        continue
                display.debug('extending task lists for all hosts with included blocks')
                for host in hosts_left:
                    iterator.add_tasks(host, all_blocks[host])
                display.debug('done extending task lists')
                display.debug('done processing included files')
            display.debug('results queue empty')
            display.debug('checking for any_errors_fatal')
            failed_hosts = []
            unreachable_hosts = []
            for res in results:
                if res.is_failed():
                    failed_hosts.append(res._host.name)
                elif res.is_unreachable():
                    unreachable_hosts.append(res._host.name)
            if (any_errors_fatal and ((len(failed_hosts) > 0) or (len(unreachable_hosts) > 0))):
                for host in hosts_left:
                    (s, _) = iterator.get_next_task_for_host(host, peek=True)
                    if ((s.run_state != iterator.ITERATING_RESCUE) or ((s.run_state == iterator.ITERATING_RESCUE) and ((s.fail_state & iterator.FAILED_RESCUE) != 0))):
                        self._tqm._failed_hosts[host.name] = True
                        result |= self._tqm.RUN_FAILED_BREAK_PLAY
            display.debug('done checking for any_errors_fatal')
            display.debug('checking for max_fail_percentage')
            if ((iterator._play.max_fail_percentage is not None) and (len(results) > 0)):
                percentage = (iterator._play.max_fail_percentage / 100.0)
                if ((len(self._tqm._failed_hosts) / len(results)) > percentage):
                    for host in hosts_left:
                        if (host.name not in failed_hosts):
                            self._tqm._failed_hosts[host.name] = True
                            iterator.mark_host_failed(host)
                    self._tqm.send_callback('v2_playbook_on_no_hosts_remaining')
                    result |= self._tqm.RUN_FAILED_BREAK_PLAY
            display.debug('done checking for max_fail_percentage')
            display.debug('checking to see if all hosts have failed and the running result is not ok')
            if ((result != self._tqm.RUN_OK) and (len(self._tqm._failed_hosts) >= len(hosts_left))):
                display.debug('^ not ok, so returning result now')
                self._tqm.send_callback('v2_playbook_on_no_hosts_remaining')
                return result
            display.debug('done checking to see if all hosts have failed')
        except (IOError, EOFError) as e:
            display.debug(('got IOError/EOFError in task loop: %s' % e))
            return self._tqm.RUN_UNKNOWN_ERROR
    return super(StrategyModule, self).run(iterator, play_context, result)
