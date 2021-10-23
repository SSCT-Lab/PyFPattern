

def _do_handler_run(self, handler, handler_name, iterator, play_context, notified_hosts=None):
    saved_name = handler.name
    handler.name = handler_name
    self._tqm.send_callback('v2_playbook_on_handler_task_start', handler)
    handler.name = saved_name
    if (notified_hosts is None):
        notified_hosts = self._notified_handlers[handler._uuid]
    run_once = False
    try:
        action = action_loader.get(handler.action, class_only=True)
        if (handler.run_once or getattr(action, 'BYPASS_HOST_LOOP', False)):
            run_once = True
    except KeyError:
        pass
    host_results = []
    for host in notified_hosts:
        if ((not handler.has_triggered(host)) and ((not iterator.is_failed(host)) or play_context.force_handlers)):
            if (handler._uuid not in iterator._task_uuid_cache):
                iterator._task_uuid_cache[handler._uuid] = handler
            task_vars = self._variable_manager.get_vars(play=iterator._play, host=host, task=handler)
            self.add_tqm_variables(task_vars, play=iterator._play)
            self._queue_task(host, handler, task_vars, play_context)
            if run_once:
                break
    host_results = self._wait_on_pending_results(iterator)
    try:
        included_files = IncludedFile.process_include_results(host_results, self._tqm, iterator=iterator, inventory=self._inventory, loader=self._loader, variable_manager=self._variable_manager)
    except AnsibleError as e:
        return False
    result = True
    if (len(included_files) > 0):
        for included_file in included_files:
            try:
                new_blocks = self._load_included_file(included_file, iterator=iterator, is_handler=True)
                for block in new_blocks:
                    iterator._play.handlers.append(block)
                    iterator.cache_block_tasks(block)
                    for task in block.block:
                        result = self._do_handler_run(handler=task, handler_name=None, iterator=iterator, play_context=play_context, notified_hosts=included_file._hosts[:])
                        if (not result):
                            break
            except AnsibleError as e:
                for host in included_file._hosts:
                    iterator.mark_host_failed(host)
                    self._tqm._failed_hosts[host.name] = True
                display.warning(str(e))
                continue
    self._notified_handlers[handler._uuid] = []
    display.debug(('done running handlers, result is: %s' % result))
    return result
