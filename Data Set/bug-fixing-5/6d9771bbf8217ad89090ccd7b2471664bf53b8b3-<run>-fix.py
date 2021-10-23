def run(self):
    super(PlaybookCLI, self).run()
    sshpass = None
    becomepass = None
    vault_pass = None
    passwords = {
        
    }
    for playbook in self.args:
        if (not os.path.exists(playbook)):
            raise AnsibleError(('the playbook: %s could not be found' % playbook))
        if (not (os.path.isfile(playbook) or stat.S_ISFIFO(os.stat(playbook).st_mode))):
            raise AnsibleError(('the playbook: %s does not appear to be a file' % playbook))
    if ((not self.options.listhosts) and (not self.options.listtasks) and (not self.options.listtags) and (not self.options.syntax)):
        self.normalize_become_options()
        (sshpass, becomepass) = self.ask_passwords()
        passwords = {
            'conn_pass': sshpass,
            'become_pass': becomepass,
        }
    loader = DataLoader()
    if self.options.vault_password_file:
        vault_pass = CLI.read_vault_password_file(self.options.vault_password_file, loader=loader)
        loader.set_vault_password(vault_pass)
    elif self.options.ask_vault_pass:
        vault_pass = self.ask_vault_passwords()[0]
        loader.set_vault_password(vault_pass)
    variable_manager = VariableManager()
    variable_manager.extra_vars = load_extra_vars(loader=loader, options=self.options)
    variable_manager.options_vars = load_options_vars(self.options)
    inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=self.options.inventory)
    variable_manager.set_inventory(inventory)
    no_hosts = False
    if (len(inventory.list_hosts()) == 0):
        display.warning('provided hosts list is empty, only localhost is available')
        no_hosts = True
    inventory.subset(self.options.subset)
    if ((len(inventory.list_hosts()) == 0) and (no_hosts is False)):
        raise AnsibleError('Specified --limit does not match any hosts')
    if self.options.flush_cache:
        for host in inventory.list_hosts():
            variable_manager.clear_facts(host)
    pbex = PlaybookExecutor(playbooks=self.args, inventory=inventory, variable_manager=variable_manager, loader=loader, options=self.options, passwords=passwords)
    results = pbex.run()
    if isinstance(results, list):
        for p in results:
            display.display(('\nplaybook: %s' % p['playbook']))
            for (idx, play) in enumerate(p['plays']):
                msg = ('\n  play #%d (%s): %s' % ((idx + 1), ','.join(play.hosts), play.name))
                mytags = set(play.tags)
                msg += ('\tTAGS: [%s]' % ','.join(mytags))
                if self.options.listhosts:
                    playhosts = set(inventory.get_hosts(play.hosts))
                    msg += ('\n    pattern: %s\n    hosts (%d):' % (play.hosts, len(playhosts)))
                    for host in playhosts:
                        msg += ('\n      %s' % host)
                display.display(msg)
                all_tags = set()
                if (self.options.listtags or self.options.listtasks):
                    taskmsg = ''
                    if self.options.listtasks:
                        taskmsg = '    tasks:\n'

                    def _process_block(b):
                        taskmsg = ''
                        for task in b.block:
                            if isinstance(task, Block):
                                taskmsg += _process_block(task)
                            else:
                                if (task.action == 'meta'):
                                    continue
                                all_tags.update(task.tags)
                                if self.options.listtasks:
                                    cur_tags = list(mytags.union(set(task.tags)))
                                    cur_tags.sort()
                                    if task.name:
                                        taskmsg += ('      %s' % task.get_name())
                                    else:
                                        taskmsg += ('      %s' % task.action)
                                    taskmsg += ('\tTAGS: [%s]\n' % ', '.join(cur_tags))
                        return taskmsg
                    all_vars = variable_manager.get_vars(loader=loader, play=play)
                    play_context = PlayContext(play=play, options=self.options)
                    for block in play.compile():
                        block = block.filter_tagged_tasks(play_context, all_vars)
                        if (not block.has_tasks()):
                            continue
                        taskmsg += _process_block(block)
                    if self.options.listtags:
                        cur_tags = list(mytags.union(all_tags))
                        cur_tags.sort()
                        taskmsg += ('      TASK TAGS: [%s]\n' % ', '.join(cur_tags))
                    display.display(taskmsg)
        return 0
    else:
        return results