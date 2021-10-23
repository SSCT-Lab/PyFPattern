def set_action(self):
    super(VaultCLI, self).set_action()
    if (self.action in self.can_output):
        self.parser.add_option('--output', default=None, dest='output_file', help='output file name for encrypt or decrypt; use - for stdout', action='callback', callback=CLI.unfrack_path, type='string')
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