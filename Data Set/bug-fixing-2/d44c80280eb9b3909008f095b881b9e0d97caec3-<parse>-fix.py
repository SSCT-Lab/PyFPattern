

def parse(self):
    self.parser = CLI.base_parser(vault_opts=True, usage=('usage: %%prog [%s] [--help] [options] vaultfile.yml' % '|'.join(self.VALID_ACTIONS)), epilog=("\nSee '%s <command> --help' for more information on a specific command.\n\n" % os.path.basename(sys.argv[0])))
    self.set_action()
    if (self.action == 'create'):
        self.parser.set_usage('usage: %prog create [options] file_name')
    elif (self.action == 'decrypt'):
        self.parser.set_usage('usage: %prog decrypt [options] file_name')
    elif (self.action == 'edit'):
        self.parser.set_usage('usage: %prog edit [options] file_name')
    elif (self.action == 'view'):
        self.parser.set_usage('usage: %prog view [options] file_name')
    elif (self.action == 'encrypt'):
        self.parser.set_usage('usage: %prog encrypt [options] file_name')
    elif (self.action == 'encrypt_string'):
        self.parser.add_option('-p', '--prompt', dest='encrypt_string_prompt', action='store_true', help='Prompt for the string to encrypt')
        self.parser.add_option('-n', '--name', dest='encrypt_string_names', action='append', help='Specify the variable name')
        self.parser.add_option('--stdin-name', dest='encrypt_string_stdin_name', default=None, help='Specify the variable name for stdin')
        self.parser.set_usage('usage: %prog encrypt-string [--prompt] [options] string_to_encrypt')
    elif (self.action == 'rekey'):
        self.parser.set_usage('usage: %prog rekey [options] file_name')
    super(VaultCLI, self).parse()
    display.verbosity = self.options.verbosity
    can_output = ['encrypt', 'decrypt', 'encrypt_string']
    if (self.action not in can_output):
        if self.options.output_file:
            raise AnsibleOptionsError(('The --output option can be used only with ansible-vault %s' % '/'.join(can_output)))
        if (len(self.args) == 0):
            raise AnsibleOptionsError('Vault requires at least one filename as a parameter')
    elif (self.options.output_file and (len(self.args) > 1)):
        raise AnsibleOptionsError('At most one input file may be used with the --output option')
    if (self.action == 'encrypt_string'):
        if (('-' in self.args) or (len(self.args) == 0) or self.options.encrypt_string_stdin_name):
            self.encrypt_string_read_stdin = True
        if (self.options.encrypt_string_prompt and self.encrypt_string_read_stdin):
            raise AnsibleOptionsError('The --prompt option is not supported if also reading input from stdin')
