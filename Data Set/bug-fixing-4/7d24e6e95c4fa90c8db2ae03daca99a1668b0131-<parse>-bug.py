def parse(self):
    ' create an options parser for bin/ansible '
    self.parser = CLI.base_parser(usage='%prog -U <repository> [options]', connect_opts=True, vault_opts=True, runtask_opts=True, subset_opts=True, inventory_opts=True, module_opts=True, runas_prompt_opts=True)
    self.parser.add_option('--purge', default=False, action='store_true', help='purge checkout after playbook run')
    self.parser.add_option('-o', '--only-if-changed', dest='ifchanged', default=False, action='store_true', help='only run the playbook if the repository has been updated')
    self.parser.add_option('-s', '--sleep', dest='sleep', default=None, help='sleep for random interval (between 0 and n number of seconds) before starting. This is a useful way to disperse git requests')
    self.parser.add_option('-f', '--force', dest='force', default=False, action='store_true', help='run the playbook even if the repository could not be updated')
    self.parser.add_option('-d', '--directory', dest='dest', default=None, help='directory to checkout repository to')
    self.parser.add_option('-U', '--url', dest='url', default=None, help='URL of the playbook repository')
    self.parser.add_option('--full', dest='fullclone', action='store_true', help='Do a full clone, instead of a shallow one.')
    self.parser.add_option('-C', '--checkout', dest='checkout', help='branch/tag/commit to checkout.  Defaults to behavior of repository module.')
    self.parser.add_option('--accept-host-key', default=False, dest='accept_host_key', action='store_true', help='adds the hostkey for the repo url if not already added')
    self.parser.add_option('-m', '--module-name', dest='module_name', default=self.DEFAULT_REPO_TYPE, help=('Repository module name, which ansible will use to check out the repo. Default is %s.' % self.DEFAULT_REPO_TYPE))
    self.parser.add_option('--verify-commit', dest='verify', default=False, action='store_true', help='verify GPG signature of checked out commit, if it fails abort running the playbook. This needs the corresponding VCS module to support such an operation')
    self.parser.set_defaults(inventory=None)
    (self.options, self.args) = self.parser.parse_args(self.args[1:])
    if (not self.options.dest):
        hostname = socket.getfqdn()
        self.options.dest = os.path.join('~/.ansible/pull', hostname)
    self.options.dest = os.path.expandvars(os.path.expanduser(self.options.dest))
    if self.options.sleep:
        try:
            secs = random.randint(0, int(self.options.sleep))
            self.options.sleep = secs
        except ValueError:
            raise AnsibleOptionsError(('%s is not a number.' % self.options.sleep))
    if (not self.options.url):
        raise AnsibleOptionsError('URL for repository not specified, use -h for help')
    if (self.options.module_name not in self.SUPPORTED_REPO_MODULES):
        raise AnsibleOptionsError(('Unsuported repo module %s, choices are %s' % (self.options.module_name, ','.join(self.SUPPORTED_REPO_MODULES))))
    display.verbosity = self.options.verbosity
    self.validate_conflicts(vault_opts=True)