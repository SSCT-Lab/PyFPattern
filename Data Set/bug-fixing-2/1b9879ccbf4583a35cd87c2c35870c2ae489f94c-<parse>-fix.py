

def parse(self):
    self.parser = CLI.base_parser(usage='usage: %prog [options] [host|group]', epilog='Show Ansible inventory information, by default it uses the inventory script JSON format', inventory_opts=True, vault_opts=True, basedir_opts=True)
    self.parser.remove_option('--limit')
    self.parser.remove_option('--list-hosts')
    action_group = optparse.OptionGroup(self.parser, 'Actions', 'One of following must be used on invocation, ONLY ONE!')
    action_group.add_option('--list', action='store_true', default=False, dest='list', help='Output all hosts info, works as inventory script')
    action_group.add_option('--host', action='store', default=None, dest='host', help='Output specific host info, works as inventory script')
    action_group.add_option('--graph', action='store_true', default=False, dest='graph', help='create inventory graph, if supplying pattern it must be a valid group name')
    self.parser.add_option_group(action_group)
    self.parser.add_option('-y', '--yaml', action='store_true', default=False, dest='yaml', help='Use YAML format instead of default JSON, ignored for --graph')
    self.parser.add_option('--vars', action='store_true', default=False, dest='show_vars', help='Add vars to graph display, ignored unless used with --graph')
    self.parser.add_option('--export', action='store_true', default=C.INVENTORY_EXPORT, dest='export', help='When doing an --list, represent in a way that is optimized for export,not as an accurate representation of how Ansible has processed it')
    super(InventoryCLI, self).parse()
    display.verbosity = self.options.verbosity
    self.validate_conflicts(vault_opts=True)
    used = 0
    for opt in (self.options.list, self.options.host, self.options.graph):
        if opt:
            used += 1
    if (used == 0):
        raise AnsibleOptionsError('No action selected, at least one of --host, --graph or --list needs to be specified.')
    elif (used > 1):
        raise AnsibleOptionsError('Conflicting options used, only one of --host, --graph or --list can be used at the same time.')
    if (len(self.args) > 0):
        self.options.pattern = self.args[0]
    else:
        self.options.pattern = 'all'
