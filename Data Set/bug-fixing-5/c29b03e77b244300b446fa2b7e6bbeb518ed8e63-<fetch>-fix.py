def fetch(self):
    result = dict(changed=True, uuid=self.vm.summary.config.uuid)
    vm_username = self.module.params['vm_username']
    vm_password = self.module.params['vm_password']
    hostname = self.module.params['hostname']
    dest = self.module.params['fetch']['dest']
    src = self.module.params['fetch']['src']
    creds = vim.vm.guest.NamePasswordAuthentication(username=vm_username, password=vm_password)
    file_manager = self.content.guestOperationsManager.fileManager
    try:
        fileTransferInfo = file_manager.InitiateFileTransferFromGuest(vm=self.vm, auth=creds, guestFilePath=src)
        url = fileTransferInfo.url
        url = url.replace('*', hostname)
        (resp, info) = urls.fetch_url(self.module, url, method='GET')
        try:
            with open(dest, 'wb') as local_file:
                local_file.write(resp.read())
        except Exception as e:
            self.module.fail_json(msg=('local file write exception : %s' % to_native(e)), uuid=self.vm.summary.config.uuid)
    except vim.fault.FileNotFound as file_not_found:
        self.module.fail_json(msg=('Guest file %s does not exist : %s' % (src, to_native(file_not_found.msg))), uuid=self.vm.summary.config.uuid)
    except vim.fault.FileFault as e:
        self.module.fail_json(msg=('FileFault : %s' % to_native(e.msg)), uuid=self.vm.summary.config.uuid)
    except vim.fault.GuestPermissionDenied:
        self.module.fail_json(msg=('Permission denied to fetch file %s' % src), uuid=self.vm.summary.config.uuid)
    except vim.fault.InvalidGuestLogin:
        self.module.fail_json(msg=('Invalid guest login for user %s' % vm_username), uuid=self.vm.summary.config.uuid)
    except Exception as e:
        self.module.fail_json(msg=('Failed to Fetch file from Vm VMware exception : %s' % to_native(e)), uuid=self.vm.summary.config.uuid)
    return result