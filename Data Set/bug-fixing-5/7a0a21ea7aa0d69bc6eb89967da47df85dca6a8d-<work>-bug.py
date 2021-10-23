def work(self):
    'Excute task '
    if (not HAS_SCP):
        self.module.fail_json(msg="'Error: No scp package, please install it.'")
    if (not HAS_PARAMIKO):
        self.module.fail_json(msg="'Error: No paramiko package, please install it.'")
    if (self.local_file and (len(self.local_file) > 4096)):
        self.module.fail_json(msg="'Error: The maximum length of local_file is 4096.'")
    if (self.remote_file and (len(self.remote_file) > 4096)):
        self.module.fail_json(msg="'Error: The maximum length of remote_file is 4096.'")
    (retcode, cur_state) = self.get_scp_enable()
    if (retcode and (cur_state == 'Disable')):
        self.module.fail_json(msg="'Error: Please ensure SCP server is enabled.'")
    if (not os.path.isfile(self.local_file)):
        self.module.fail_json(msg='Local file {0} not found'.format(self.local_file))
    dest = (self.remote_file or ('/' + os.path.basename(self.local_file)))
    (remote_exists, file_size) = self.remote_file_exists(dest, file_system=self.file_system)
    if (remote_exists and (os.path.getsize(self.local_file) != file_size)):
        remote_exists = False
    if (not remote_exists):
        self.changed = True
        file_exists = False
    else:
        file_exists = True
        self.transfer_result = 'The local file already exists on the device.'
    if (not file_exists):
        self.transfer_file(dest)
        self.transfer_result = 'The local file has been successfully transferred to the device.'
    if (self.remote_file is None):
        self.remote_file = ('/' + os.path.basename(self.local_file))
    self.module.exit_json(changed=self.changed, transfer_result=self.transfer_result, local_file=self.local_file, remote_file=self.remote_file, file_system=self.file_system)