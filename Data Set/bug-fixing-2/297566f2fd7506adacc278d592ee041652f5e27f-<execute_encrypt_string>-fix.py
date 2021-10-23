

def execute_encrypt_string(self):
    b_plaintext = None
    b_plaintext_list = []
    args = [x for x in self.args if (x != '-')]
    if self.options.encrypt_string_prompt:
        msg = 'String to encrypt: '
        name = None
        name_prompt_response = display.prompt('Variable name (enter for no name): ')
        if (name_prompt_response != ''):
            name = name_prompt_response
        prompt_response = display.prompt(msg)
        if (prompt_response == ''):
            raise AnsibleOptionsError('The plaintext provided from the prompt was empty, not encrypting')
        b_plaintext = to_bytes(prompt_response)
        b_plaintext_list.append((b_plaintext, self.FROM_PROMPT, name))
    if self.encrypt_string_read_stdin:
        if sys.stdout.isatty():
            display.display('Reading plaintext input from stdin. (ctrl-d to end input)', stderr=True)
        stdin_text = sys.stdin.read()
        if (stdin_text == ''):
            raise AnsibleOptionsError('stdin was empty, not encrypting')
        b_plaintext = to_bytes(stdin_text)
        name = self.options.encrypt_string_stdin_name
        b_plaintext_list.append((b_plaintext, self.FROM_STDIN, name))
    if (hasattr(self.options, 'encrypt_string_names') and self.options.encrypt_string_names):
        name_and_text_list = list(zip(self.options.encrypt_string_names, args))
        if (len(args) > len(name_and_text_list)):
            display.display('The number of --name options do not match the number of args.', stderr=True)
            display.display(('The last named variable will be "%s". The rest will not have names.' % self.options.encrypt_string_names[(- 1)]), stderr=True)
        for extra_arg in args[len(name_and_text_list):]:
            name_and_text_list.append((None, extra_arg))
    else:
        name_and_text_list = [(None, x) for x in args]
    for name_and_text in name_and_text_list:
        (name, plaintext) = name_and_text
        if (plaintext == ''):
            raise AnsibleOptionsError('The plaintext provided from the command line args was empty, not encrypting')
        b_plaintext = to_bytes(plaintext)
        b_plaintext_list.append((b_plaintext, self.FROM_ARGS, name))
    outputs = self._format_output_vault_strings(b_plaintext_list)
    for output in outputs:
        err = output.get('err', None)
        out = output.get('out', '')
        if err:
            sys.stderr.write(err)
        print(out)
    if sys.stdout.isatty():
        display.display('Encryption successful', stderr=True)
