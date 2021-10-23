def ssh_key_has_changed(self):
    ssh_key_name = self.module.params.get('ssh_key')
    if (ssh_key_name is None):
        return False
    param_ssh_key_fp = self.get_ssh_keypair(key='fingerprint')
    instance_ssh_key_name = self.instance.get('keypair')
    if (instance_ssh_key_name is None):
        return True
    instance_ssh_key_fp = self.get_ssh_keypair(key='fingerprint', name=instance_ssh_key_name, fail_on_missing=False)
    if (not instance_ssh_key_fp):
        return True
    if (instance_ssh_key_fp != param_ssh_key_fp):
        return True
    return False