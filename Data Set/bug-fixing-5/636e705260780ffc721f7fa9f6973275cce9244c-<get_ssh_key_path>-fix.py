def get_ssh_key_path(self):
    info = self.user_info()
    if os.path.isabs(self.ssh_file):
        ssh_key_file = self.ssh_file
    else:
        if ((not os.path.exists(info[5])) and (not self.module.check_mode)):
            raise Exception(('User %s home directory does not exist' % self.name))
        ssh_key_file = os.path.join(info[5], self.ssh_file)
    return ssh_key_file