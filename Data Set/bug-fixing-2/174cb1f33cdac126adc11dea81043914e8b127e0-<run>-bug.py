

def run(self):
    super(VaultCLI, self).run()
    loader = DataLoader()
    old_umask = os.umask(63)
    vault_ids = self.options.vault_ids
    default_vault_ids = C.DEFAULT_VAULT_IDENTITY_LIST
    vault_ids = (default_vault_ids + vault_ids)
    if (self.action in ['decrypt', 'view', 'rekey', 'edit']):
        vault_secrets = self.setup_vault_secrets(loader, vault_ids=vault_ids, vault_password_files=self.options.vault_password_files, ask_vault_pass=self.options.ask_vault_pass)
        if (not vault_secrets):
            raise AnsibleOptionsError("A vault password is required to use Ansible's Vault")
    if (self.action in ['encrypt', 'encrypt_string', 'create']):
        if (len(vault_ids) > 1):
            raise AnsibleOptionsError('Only one --vault-id can be used for encryption')
        vault_secrets = None
        vault_secrets = self.setup_vault_secrets(loader, vault_ids=vault_ids, vault_password_files=self.options.vault_password_files, ask_vault_pass=self.options.ask_vault_pass, create_new_password=True)
        if (not vault_secrets):
            raise AnsibleOptionsError("A vault password is required to use Ansible's Vault")
        encrypt_secret = match_encrypt_secret(vault_secrets)
        self.encrypt_vault_id = encrypt_secret[0]
        self.encrypt_secret = encrypt_secret[1]
    if (self.action in ['rekey']):
        new_vault_ids = []
        if self.options.new_vault_id:
            new_vault_ids.append(self.options.new_vault_id)
        new_vault_secrets = self.setup_vault_secrets(loader, vault_ids=new_vault_ids, vault_password_files=self.options.new_vault_password_files, ask_vault_pass=self.options.ask_vault_pass, create_new_password=True)
        if (not new_vault_secrets):
            raise AnsibleOptionsError("A new vault password is required to use Ansible's Vault rekey")
        new_encrypt_secret = match_encrypt_secret(new_vault_secrets)
        self.new_encrypt_vault_id = new_encrypt_secret[0]
        self.new_encrypt_secret = new_encrypt_secret[1]
    loader.set_vault_secrets(vault_secrets)
    vault = VaultLib(vault_secrets)
    self.editor = VaultEditor(vault)
    self.execute()
    os.umask(old_umask)
