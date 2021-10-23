

def copy(self):
    result = dict(changed=True, uuid=self.vm.summary.config.uuid)
    vm_username = self.module.params['vm_username']
    vm_password = self.module.params['vm_password']
    hostname = self.module.params['hostname']
    overwrite = self.module.params['copy']['overwrite']
    dest = self.module.params['copy']['dest']
    src = self.module.params['copy']['src']
    b_src = to_bytes(src, errors='surrogate_or_strict')
    if (not os.path.exists(b_src)):
        self.module.fail_json(msg=('Source %s not found' % src))
    if (not os.access(b_src, os.R_OK)):
        self.module.fail_json(msg=('Source %s not readable' % src))
    if os.path.isdir(b_src):
        self.module.fail_json(msg=('copy does not support copy of directory: %s' % src))
    data = None
    with open(b_src, 'rb') as local_file:
        data = local_file.read()
    file_size = os.path.getsize(b_src)
    creds = vim.vm.guest.NamePasswordAuthentication(username=vm_username, password=vm_password)
    file_attributes = vim.vm.guest.FileManager.FileAttributes()
    file_manager = self.content.guestOperationsManager.fileManager
    try:
        url = file_manager.InitiateFileTransferToGuest(vm=self.vm, auth=creds, guestFilePath=dest, fileAttributes=file_attributes, overwrite=overwrite, fileSize=file_size)
        url = url.replace('*', hostname)
        (resp, info) = urls.fetch_url(self.module, url, data=data, method='PUT')
        status_code = info['status']
        if (status_code != 200):
            self.module.fail_json(msg=('problem during file transfer, http message:%s' % info), uuid=self.vm.summary.config.uuid)
    except vim.fault.FileAlreadyExists:
        result['changed'] = False
        result['msg'] = ('Guest file %s already exists' % dest)
        return result
    except vim.fault.FileFault as e:
        self.module.fail_json(msg=('FileFault:%s' % to_native(e.msg)), uuid=self.vm.summary.config.uuid)
    except vim.fault.GuestPermissionDenied as permission_denied:
        self.module.fail_json(msg=('Permission denied to copy file into destination %s : %s' % (dest, to_native(permission_denied.msg))), uuid=self.vm.summary.config.uuid)
    except vim.fault.InvalidGuestLogin as invalid_guest_login:
        self.module.fail_json(msg=('Invalid guest login for user %s : %s' % (vm_username, to_native(invalid_guest_login.msg))))
    except Exception as e:
        self.module.fail_json(msg=('Failed to Copy file to Vm VMware exception : %s' % to_native(e)), uuid=self.vm.summary.config.uuid)
    return result
