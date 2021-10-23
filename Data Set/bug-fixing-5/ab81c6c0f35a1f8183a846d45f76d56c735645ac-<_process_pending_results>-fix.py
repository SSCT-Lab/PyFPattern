def _process_pending_results(self, iterator, one_pass=False, max_passes=None):
    '\n        Reads results off the final queue and takes appropriate action\n        based on the result (executing callbacks, updating state, etc.).\n        '
    ret_results = []

    def get_original_host(host_name):
        host_name = to_text(host_name)
        if (host_name in self._inventory.hosts):
            return self._inventory.hosts[host_name]
        else:
            return self._inventory.get_host(host_name)

    def search_handler_blocks_by_name(handler_name, handler_blocks):
        for handler_block in handler_blocks:
            for handler_task in handler_block.block:
                if handler_task.name:
                    handler_vars = self._variable_manager.get_vars(play=iterator._play, task=handler_task)
                    templar = Templar(loader=self._loader, variables=handler_vars)
                    try:
                        target_handler_name = templar.template(handler_task.name)
                        if (target_handler_name == handler_name):
                            return handler_task
                        else:
                            target_handler_name = templar.template(handler_task.get_name())
                            if (target_handler_name == handler_name):
                                return handler_task
                    except (UndefinedError, AnsibleUndefinedVariable):
                        continue
        return None

    def search_handler_blocks_by_uuid(handler_uuid, handler_blocks):
        for handler_block in handler_blocks:
            for handler_task in handler_block.block:
                if (handler_uuid == handler_task._uuid):
                    return handler_task
        return None

    def parent_handler_match(target_handler, handler_name):
        if target_handler:
            if isinstance(target_handler, (TaskInclude, IncludeRole)):
                try:
                    handler_vars = self._variable_manager.get_vars(play=iterator._play, task=target_handler)
                    templar = Templar(loader=self._loader, variables=handler_vars)
                    target_handler_name = templar.template(target_handler.name)
                    if (target_handler_name == handler_name):
                        return True
                    else:
                        target_handler_name = templar.template(target_handler.get_name())
                        if (target_handler_name == handler_name):
                            return True
                except (UndefinedError, AnsibleUndefinedVariable):
                    pass
            return parent_handler_match(target_handler._parent, handler_name)
        else:
            return False
    cur_pass = 0
    while True:
        try:
            self._results_lock.acquire()
            task_result = self._results.popleft()
        except IndexError:
            break
        finally:
            self._results_lock.release()
        original_host = get_original_host(task_result._host)
        found_task = iterator.get_original_task(original_host, task_result._task)
        original_task = found_task.copy(exclude_parent=True, exclude_tasks=True)
        original_task._parent = found_task._parent
        original_task.from_attrs(task_result._task_fields)
        task_result._host = original_host
        task_result._task = original_task
        if original_task.loop_control:
            loop_var = (original_task.loop_control.loop_var or 'item')
        else:
            loop_var = 'item'
        if ('_ansible_retry' in task_result._result):
            self._tqm.send_callback('v2_runner_retry', task_result)
            continue
        elif ('_ansible_item_result' in task_result._result):
            if (task_result.is_failed() or task_result.is_unreachable()):
                self._tqm.send_callback('v2_runner_item_on_failed', task_result)
            elif task_result.is_skipped():
                self._tqm.send_callback('v2_runner_item_on_skipped', task_result)
            else:
                if ('diff' in task_result._result):
                    if self._diff:
                        self._tqm.send_callback('v2_on_file_diff', task_result)
                self._tqm.send_callback('v2_runner_item_on_ok', task_result)
            continue
        if original_task.register:
            host_list = self.get_task_hosts(iterator, original_host, original_task)
            clean_copy = strip_internal_keys(task_result._result)
            if ('invocation' in clean_copy):
                del clean_copy['invocation']
            for target_host in host_list:
                self._variable_manager.set_nonpersistent_facts(target_host, {
                    original_task.register: clean_copy,
                })
        role_ran = False
        if task_result.is_failed():
            role_ran = True
            ignore_errors = original_task.ignore_errors
            if (not ignore_errors):
                display.debug(('marking %s as failed' % original_host.name))
                if original_task.run_once:
                    for h in self._inventory.get_hosts(iterator._play.hosts):
                        if (h.name not in self._tqm._unreachable_hosts):
                            (state, _) = iterator.get_next_task_for_host(h, peek=True)
                            iterator.mark_host_failed(h)
                            (state, new_task) = iterator.get_next_task_for_host(h, peek=True)
                else:
                    iterator.mark_host_failed(original_host)
                self._tqm._stats.increment('failures', original_host.name)
                (state, _) = iterator.get_next_task_for_host(original_host, peek=True)
                if (iterator.is_failed(original_host) and state and (state.run_state == iterator.ITERATING_COMPLETE)):
                    self._tqm._failed_hosts[original_host.name] = True
                if (state and (state.run_state == iterator.ITERATING_RESCUE)):
                    self._variable_manager.set_nonpersistent_facts(original_host, dict(ansible_failed_task=original_task.serialize(), ansible_failed_result=task_result._result))
            else:
                self._tqm._stats.increment('ok', original_host.name)
                if (('changed' in task_result._result) and task_result._result['changed']):
                    self._tqm._stats.increment('changed', original_host.name)
            self._tqm.send_callback('v2_runner_on_failed', task_result, ignore_errors=ignore_errors)
        elif task_result.is_unreachable():
            self._tqm._unreachable_hosts[original_host.name] = True
            iterator._play._removed_hosts.append(original_host.name)
            self._tqm._stats.increment('dark', original_host.name)
            self._tqm.send_callback('v2_runner_on_unreachable', task_result)
        elif task_result.is_skipped():
            self._tqm._stats.increment('skipped', original_host.name)
            self._tqm.send_callback('v2_runner_on_skipped', task_result)
        else:
            role_ran = True
            if original_task.loop:
                result_items = task_result._result.get('results', [])
            else:
                result_items = [task_result._result]
            for result_item in result_items:
                if ('_ansible_notify' in result_item):
                    if task_result.is_changed():
                        for handler_name in result_item['_ansible_notify']:
                            found = False
                            target_handler = search_handler_blocks_by_name(handler_name, iterator._play.handlers)
                            if (target_handler is not None):
                                found = True
                                if (target_handler._uuid not in self._notified_handlers):
                                    self._notified_handlers[target_handler._uuid] = []
                                if (original_host not in self._notified_handlers[target_handler._uuid]):
                                    self._notified_handlers[target_handler._uuid].append(original_host)
                                    display.vv(('NOTIFIED HANDLER %s' % (handler_name,)))
                            else:
                                for target_handler_uuid in self._notified_handlers:
                                    target_handler = search_handler_blocks_by_uuid(target_handler_uuid, iterator._play.handlers)
                                    if (target_handler and parent_handler_match(target_handler, handler_name)):
                                        found = True
                                        if (original_host not in self._notified_handlers[target_handler._uuid]):
                                            self._notified_handlers[target_handler._uuid].append(original_host)
                                            display.vv(('NOTIFIED HANDLER %s' % (target_handler.get_name(),)))
                            if (handler_name in self._listening_handlers):
                                for listening_handler_uuid in self._listening_handlers[handler_name]:
                                    listening_handler = search_handler_blocks_by_uuid(listening_handler_uuid, iterator._play.handlers)
                                    if (listening_handler is not None):
                                        found = True
                                    else:
                                        continue
                                    if (original_host not in self._notified_handlers[listening_handler._uuid]):
                                        self._notified_handlers[listening_handler._uuid].append(original_host)
                                        display.vv(('NOTIFIED HANDLER %s' % (listening_handler.get_name(),)))
                            if (not found):
                                msg = ("The requested handler '%s' was not found in either the main handlers list nor in the listening handlers list" % handler_name)
                                if C.ERROR_ON_MISSING_HANDLER:
                                    raise AnsibleError(msg)
                                else:
                                    display.warning(msg)
                if ('add_host' in result_item):
                    new_host_info = result_item.get('add_host', dict())
                    self._add_host(new_host_info, iterator)
                elif ('add_group' in result_item):
                    self._add_group(original_host, result_item)
                if ('ansible_facts' in result_item):
                    if ((original_task.delegate_to is not None) and original_task.delegate_facts):
                        host_list = self.get_delegated_hosts(result_item, original_task)
                    else:
                        host_list = self.get_task_hosts(iterator, original_host, original_task)
                    if (original_task.action == 'include_vars'):
                        for (var_name, var_value) in iteritems(result_item['ansible_facts']):
                            for target_host in host_list:
                                self._variable_manager.set_host_variable(target_host, var_name, var_value)
                    else:
                        cacheable = result_item.pop('ansible_facts_cacheable', True)
                        for target_host in host_list:
                            if cacheable:
                                self._variable_manager.set_host_facts(target_host, result_item['ansible_facts'].copy())
                            self._variable_manager.set_nonpersistent_facts(target_host, result_item['ansible_facts'].copy())
                if (('ansible_stats' in result_item) and ('data' in result_item['ansible_stats']) and result_item['ansible_stats']['data']):
                    if (('per_host' not in result_item['ansible_stats']) or result_item['ansible_stats']['per_host']):
                        host_list = self.get_task_hosts(iterator, original_host, original_task)
                    else:
                        host_list = [None]
                    data = result_item['ansible_stats']['data']
                    aggregate = (('aggregate' in result_item['ansible_stats']) and result_item['ansible_stats']['aggregate'])
                    for myhost in host_list:
                        for k in data.keys():
                            if aggregate:
                                self._tqm._stats.update_custom_stats(k, data[k], myhost)
                            else:
                                self._tqm._stats.set_custom_stats(k, data[k], myhost)
            if ('diff' in task_result._result):
                if self._diff:
                    self._tqm.send_callback('v2_on_file_diff', task_result)
            if (not isinstance(original_task, TaskInclude)):
                self._tqm._stats.increment('ok', original_host.name)
                if (('changed' in task_result._result) and task_result._result['changed']):
                    self._tqm._stats.increment('changed', original_host.name)
            self._tqm.send_callback('v2_runner_on_ok', task_result)
        self._pending_results -= 1
        if (original_host.name in self._blocked_hosts):
            del self._blocked_hosts[original_host.name]
        if ((original_task._role is not None) and role_ran):
            for (entry, role_obj) in iteritems(iterator._play.ROLE_CACHE[original_task._role._role_name]):
                if (role_obj._uuid == original_task._role._uuid):
                    role_obj._had_task_run[original_host.name] = True
        ret_results.append(task_result)
        if (one_pass or ((max_passes is not None) and ((cur_pass + 1) >= max_passes))):
            break
        cur_pass += 1
    return ret_results