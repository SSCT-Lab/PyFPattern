def run(self):
    super(VaultCLI, self).run()
    loader = DataLoader()
    old_umask = os.umask(63)
    if self.options.vault_password_file:
        self.b_vault_pass = CLI.read_vault_password_file(self.options.vault_password_file, loader)
    if self.options.new_vault_password_file:
        self.b_new_vault_pass = CLI.read_vault_password_file(self.options.new_vault_password_file, loader)
    if ((not self.b_vault_pass) or self.options.ask_vault_pass):
        self.b_vault_pass = self.ask_vault_passwords()
    if (not self.b_vault_pass):
        raise AnsibleOptionsError("A password is required to use Ansible's Vault")
    if (self.action == 'rekey'):
        if (not self.b_new_vault_pass):
            self.b_new_vault_pass = self.ask_new_vault_passwords()
        if (not self.b_new_vault_pass):
            raise AnsibleOptionsError("A password is required to rekey Ansible's Vault")
    if (self.action == 'encrypt_string'):
        if self.options.encrypt_string_prompt:
            self.encrypt_string_prompt = True
    self.editor = VaultEditor(self.b_vault_pass)
    self.execute()
    os.umask(old_umask)