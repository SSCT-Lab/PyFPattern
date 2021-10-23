def _execute_meta(self, task, play_context, iterator, target_host):
    meta_action = task.args.get('_raw_params')

    def _evaluate_conditional(h):
        all_vars = self._variable_manager.get_vars(play=iterator._play, host=h, task=task)
        templar = Templar(loader=self._loader, variables=all_vars)
        return task.evaluate_conditional(templar, all_vars)
    skipped = False
    msg = ''
    if (meta_action == 'noop'):
        msg = 'noop'
    elif (meta_action == 'flush_handlers'):
        self.run_handlers(iterator, play_context)
        msg = 'ran handlers'
    elif (meta_action == 'refresh_inventory'):
        self._inventory.refresh_inventory()
        msg = 'inventory successfully refreshed'
    elif (meta_action == 'clear_facts'):
        if _evaluate_conditional(target_host):
            for host in self._inventory.get_hosts(iterator._play.hosts):
                hostname = host.get_name()
                self._variable_manager.clear_facts(hostname)
            msg = 'facts cleared'
        else:
            skipped = True
    elif (meta_action == 'clear_host_errors'):
        if _evaluate_conditional(target_host):
            for host in self._inventory.get_hosts(iterator._play.hosts):
                self._tqm._failed_hosts.pop(host.name, False)
                self._tqm._unreachable_hosts.pop(host.name, False)
                iterator._host_states[host.name].fail_state = iterator.FAILED_NONE
            msg = 'cleared host errors'
        else:
            skipped = True
    elif (meta_action == 'end_play'):
        if _evaluate_conditional(target_host):
            for host in self._inventory.get_hosts(iterator._play.hosts):
                if (host.name not in self._tqm._unreachable_hosts):
                    iterator._host_states[host.name].run_state = iterator.ITERATING_COMPLETE
            msg = 'ending play'
    elif (meta_action == 'reset_connection'):
        if (target_host in self._active_connections):
            connection = Connection(self._active_connections[target_host])
            del self._active_connections[target_host]
        else:
            connection = connection_loader.get(play_context.connection, play_context, os.devnull)
            play_context.set_options_from_plugin(connection)
        if connection:
            try:
                connection.reset()
                msg = 'reset connection'
            except ConnectionError as e:
                display.debug(('got an error while closing persistent connection: %s' % e))
        else:
            msg = 'no connection, nothing to reset'
    else:
        raise AnsibleError(('invalid meta action requested: %s' % meta_action), obj=task._ds)
    result = {
        'msg': msg,
    }
    if skipped:
        result['skipped'] = True
    else:
        result['changed'] = False
    display.vv(('META: %s' % msg))
    return [TaskResult(target_host, task, result)]