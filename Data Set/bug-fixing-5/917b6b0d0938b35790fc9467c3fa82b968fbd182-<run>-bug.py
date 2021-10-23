def run(self):
    ' create and execute the single task playbook '
    super(AdHocCLI, self).run()
    pattern = to_text(self.args[0], errors='surrogate_or_strict')
    sshpass = None
    becomepass = None
    self.normalize_become_options()
    (sshpass, becomepass) = self.ask_passwords()
    passwords = {
        'conn_pass': sshpass,
        'become_pass': becomepass,
    }
    get_all_plugin_loaders()
    (loader, inventory, variable_manager) = self._play_prereqs(self.options)
    try:
        hosts = CLI.get_host_list(inventory, self.options.subset, pattern)
    except AnsibleError:
        if self.options.subset:
            raise
        else:
            hosts = []
            display.warning('No hosts matched, nothing to do')
    if self.options.listhosts:
        display.display(('  hosts (%d):' % len(hosts)))
        for host in hosts:
            display.display(('    %s' % host))
        return 0
    if ((self.options.module_name in C.MODULE_REQUIRE_ARGS) and (not self.options.module_args)):
        err = ('No argument passed to %s module' % self.options.module_name)
        if pattern.endswith('.yml'):
            err = (err + ' (did you mean to run ansible-playbook?)')
        raise AnsibleOptionsError(err)
    play_ds = self._play_ds(pattern, self.options.seconds, self.options.poll_interval)
    play = Play().load(play_ds, variable_manager=variable_manager, loader=loader)
    playbook = Playbook(loader)
    playbook._entries.append(play)
    playbook._file_name = '__adhoc_playbook__'
    if self.callback:
        cb = self.callback
    elif self.options.one_line:
        cb = 'oneline'
    elif (C.DEFAULT_LOAD_CALLBACK_PLUGINS and (C.DEFAULT_STDOUT_CALLBACK != 'default')):
        cb = C.DEFAULT_STDOUT_CALLBACK
    else:
        cb = 'minimal'
    run_tree = False
    if self.options.tree:
        C.DEFAULT_CALLBACK_WHITELIST.append('tree')
        C.TREE_DIR = self.options.tree
        run_tree = True
    self._tqm = None
    try:
        self._tqm = TaskQueueManager(inventory=inventory, variable_manager=variable_manager, loader=loader, options=self.options, passwords=passwords, stdout_callback=cb, run_additional_callbacks=C.DEFAULT_LOAD_CALLBACK_PLUGINS, run_tree=run_tree)
        self._tqm.send_callback('v2_playbook_on_start', playbook)
        result = self._tqm.run(play)
        self._tqm.send_callback('v2_playbook_on_stats', self._tqm._stats)
    finally:
        if self._tqm:
            self._tqm.cleanup()
        if loader:
            loader.cleanup_all_tmp_files()
    return result