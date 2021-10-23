def run(self, iterator, play_context):
    '\n        The "free" strategy is a bit more complex, in that it allows tasks to\n        be sent to hosts as quickly as they can be processed. This means that\n        some hosts may finish very quickly if run tasks result in little or no\n        work being done versus other systems.\n\n        The algorithm used here also tries to be more "fair" when iterating\n        through hosts by remembering the last host in the list to be given a task\n        and starting the search from there as opposed to the top of the hosts\n        list again, which would end up favoring hosts near the beginning of the\n        list.\n        '
    last_host = 0
    result = True
    work_to_do = True
    while (work_to_do and (not self._tqm._terminated)):
        hosts_left = [host for host in self._inventory.get_hosts(iterator._play.hosts) if (host.name not in self._tqm._unreachable_hosts)]
        if (len(hosts_left) == 0):
            self._tqm.send_callback('v2_playbook_on_no_hosts_remaining')
            result = False
            break
        work_to_do = False
        starting_host = last_host
        host_results = []
        while True:
            host = hosts_left[last_host]
            display.debug(('next free host: %s' % host))
            host_name = host.get_name()
            (state, task) = iterator.get_next_task_for_host(host, peek=True)
            display.debug(('free host state: %s' % state))
            display.debug(('free host task: %s' % task))
            if ((host_name not in self._tqm._unreachable_hosts) and task):
                work_to_do = True
                display.debug('this host has work to do')
                if ((host_name not in self._blocked_hosts) or (not self._blocked_hosts[host_name])):
                    self._blocked_hosts[host_name] = True
                    (state, task) = iterator.get_next_task_for_host(host)
                    try:
                        action = action_loader.get(task.action, class_only=True)
                    except KeyError:
                        action = None
                    display.debug('getting variables')
                    task_vars = self._variable_manager.get_vars(loader=self._loader, play=iterator._play, host=host, task=task)
                    self.add_tqm_variables(task_vars, play=iterator._play)
                    templar = Templar(loader=self._loader, variables=task_vars)
                    display.debug('done getting variables')
                    try:
                        task.name = text_type(templar.template(task.name, fail_on_undefined=False))
                        display.debug('done templating')
                    except:
                        display.debug('templating failed for some reason')
                        pass
                    run_once = (templar.template(task.run_once) or (action and getattr(action, 'BYPASS_HOST_LOOP', False)))
                    if run_once:
                        if (action and getattr(action, 'BYPASS_HOST_LOOP', False)):
                            raise AnsibleError(("The '%s' module bypasses the host loop, which is currently not supported in the free strategy and would instead execute for every host in the inventory list." % task.action), obj=task._ds)
                        else:
                            display.warning('Using run_once with the free strategy is not currently supported. This task will still be executed for every host in the inventory list.')
                    if (task._role and task._role.has_run(host)):
                        if ((task._role._metadata is None) or (task._role._metadata and (not task._role._metadata.allow_duplicates))):
                            display.debug(("'%s' skipped because role has already run" % task))
                            del self._blocked_hosts[host_name]
                            continue
                    if (task.action == 'meta'):
                        self._execute_meta(task, play_context, iterator)
                        self._blocked_hosts[host_name] = False
                    elif ((not self._step) or self._take_step(task, host_name)):
                        if task.any_errors_fatal:
                            display.warning('Using any_errors_fatal with the free strategy is not supported, as tasks are executed independently on each host')
                        self._tqm.send_callback('v2_playbook_on_task_start', task, is_conditional=False)
                        self._queue_task(host, task, task_vars, play_context)
                else:
                    display.debug(('%s is blocked, skipping for now' % host_name))
            last_host += 1
            if (last_host > (len(hosts_left) - 1)):
                last_host = 0
            if (last_host == starting_host):
                break
        results = self._process_pending_results(iterator)
        host_results.extend(results)
        try:
            included_files = IncludedFile.process_include_results(host_results, self._tqm, iterator=iterator, inventory=self._inventory, loader=self._loader, variable_manager=self._variable_manager)
        except AnsibleError as e:
            return False
        if (len(included_files) > 0):
            all_blocks = dict(((host, []) for host in hosts_left))
            for included_file in included_files:
                display.debug(('collecting new blocks for %s' % included_file))
                try:
                    new_blocks = self._load_included_file(included_file, iterator=iterator)
                except AnsibleError as e:
                    for host in included_file._hosts:
                        iterator.mark_host_failed(host)
                    display.warning(str(e))
                    continue
                for new_block in new_blocks:
                    task_vars = self._variable_manager.get_vars(loader=self._loader, play=iterator._play, task=included_file._task)
                    final_block = new_block.filter_tagged_tasks(play_context, task_vars)
                    for host in hosts_left:
                        if (host in included_file._hosts):
                            all_blocks[host].append(final_block)
                display.debug(('done collecting new blocks for %s' % included_file))
            display.debug(('adding all collected blocks from %d included file(s) to iterator' % len(included_files)))
            for host in hosts_left:
                iterator.add_tasks(host, all_blocks[host])
            display.debug('done adding collected blocks to iterator')
        time.sleep(0.001)
    results = self._wait_on_pending_results(iterator)
    return super(StrategyModule, self).run(iterator, play_context, result)