def run(self, play):
    '\n        Iterates over the roles/tasks in a play, using the given (or default)\n        strategy for queueing tasks. The default is the linear strategy, which\n        operates like classic Ansible by keeping all hosts in lock-step with\n        a given task (meaning no hosts move on to the next task until all hosts\n        are done with the current task).\n        '
    if (not self._callbacks_loaded):
        self.load_callbacks()
    all_vars = self._variable_manager.get_vars(loader=self._loader, play=play)
    templar = Templar(loader=self._loader, variables=all_vars)
    new_play = play.copy()
    new_play.post_validate(templar)
    new_play.handlers = (new_play.compile_roles_handlers() + new_play.handlers)
    self.hostvars = HostVars(inventory=self._inventory, variable_manager=self._variable_manager, loader=self._loader)
    num_hosts = len(self._inventory.get_hosts(new_play.hosts, ignore_restrictions=True))
    max_serial = 0
    if new_play.serial:
        serial_items = new_play.serial
        if (not isinstance(serial_items, list)):
            serial_items = [serial_items]
        max_serial = max([pct_to_int(x, num_hosts) for x in serial_items])
    contenders = [self._options.forks, max_serial, num_hosts]
    contenders = [v for v in contenders if ((v is not None) and (v > 0))]
    self._initialize_processes(min(contenders))
    play_context = PlayContext(new_play, self._options, self.passwords, self._connection_lockfile.fileno())
    for callback_plugin in self._callback_plugins:
        if hasattr(callback_plugin, 'set_play_context'):
            callback_plugin.set_play_context(play_context)
    self.send_callback('v2_playbook_on_play_start', new_play)
    self._initialize_notified_handlers(new_play)
    strategy = strategy_loader.get(new_play.strategy, self)
    if (strategy is None):
        raise AnsibleError(('Invalid play strategy specified: %s' % new_play.strategy), obj=play._ds)
    iterator = PlayIterator(inventory=self._inventory, play=new_play, play_context=play_context, variable_manager=self._variable_manager, all_vars=all_vars, start_at_done=self._start_at_done)
    for host_name in self._failed_hosts.keys():
        host = self._inventory.get_host(host_name)
        iterator.mark_host_failed(host)
    self.clear_failed_hosts()
    if ((getattr(self._options, 'start_at_task', None) is not None) and (play_context.start_at_task is None)):
        self._start_at_done = True
    play_return = strategy.run(iterator, play_context)
    for host_name in iterator.get_failed_hosts():
        self._failed_hosts[host_name] = True
    strategy.cleanup()
    self._cleanup_processes()
    return play_return