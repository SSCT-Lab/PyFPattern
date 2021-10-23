

def parse(self):
    self.parser = CLI.base_parser(usage='usage: %prog [-l|-F|-s] [options] [-t <plugin type] [plugin]', module_opts=True, desc='plugin documentation tool', epilog='See man pages for Ansible CLI options or website for tutorials https://docs.ansible.com')
    self.parser.add_option('-F', '--list_files', action='store_true', default=False, dest='list_files', help='Show plugin names and their source files without summaries (implies --list)')
    self.parser.add_option('-l', '--list', action='store_true', default=False, dest='list_dir', help='List available plugins')
    self.parser.add_option('-s', '--snippet', action='store_true', default=False, dest='show_snippet', help='Show playbook snippet for specified plugin(s)')
    self.parser.add_option('-a', '--all', action='store_true', default=False, dest='all_plugins', help='**For internal testing only** Show documentation for all plugins.')
    self.parser.add_option('-t', '--type', action='store', default='module', dest='type', type='choice', help='Choose which plugin type (defaults to "module")', choices=['cache', 'callback', 'connection', 'inventory', 'lookup', 'module', 'strategy', 'vars'])
    super(DocCLI, self).parse()
    if ([self.options.all_plugins, self.options.list_dir, self.options.list_files, self.options.show_snippet].count(True) > 1):
        raise AnsibleOptionsError('Only one of -l, -F, -s or -a can be used at the same time.')
    display.verbosity = self.options.verbosity
