def ssh_key_has_changed(self):
    ssh_key_name = self.module.params.get('ssh_key')
    if (ssh_key_name is None):
        return False
    instance_ssh_key_name = self.instance.get('keypair')
    if (instance_ssh_key_name is None):
        return True
    if (ssh_key_name == instance_ssh_key_name):
        return False
    res = self.cs.listSSHKeyPairs(name=instance_ssh_key_name)
    instance_ssh_key = res['sshkeypair'][0]
    res = self.cs.listSSHKeyPairs(name=ssh_key_name)
    param_ssh_key = res['sshkeypair'][0]
    if (param_ssh_key['fingerprint'] != instance_ssh_key['fingerprint']):
        return True
    return False