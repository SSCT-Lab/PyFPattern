def execute_create(self):
    ' create and open a file in an editor that will be encrypted with the provided vault secret when closed'
    if (len(self.args) > 1):
        raise AnsibleOptionsError('ansible-vault create can take only one filename argument')
    self.editor.create_file(self.args[0], self.encrypt_secret, vault_id=self.encrypt_vault_id)