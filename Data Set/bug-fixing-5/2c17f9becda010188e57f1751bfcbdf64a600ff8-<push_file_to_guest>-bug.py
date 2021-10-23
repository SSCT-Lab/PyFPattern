def push_file_to_guest(self, vm, username, password, src, dest, overwrite=True):
    " Use VMWare's filemanager api to push a file over http "
    result = {
        'failed': False,
    }
    tools_status = vm.guest.toolsStatus
    if ((tools_status == 'toolsNotInstalled') or (tools_status == 'toolsNotRunning')):
        result['failed'] = True
        result['msg'] = 'VMwareTools is not installed or is not running in the guest'
        return result
    creds = vim.vm.guest.NamePasswordAuthentication(username=username, password=password)
    filesize = None
    fdata = None
    try:
        filesize = os.stat(src).st_size
        fdata = None
        with open(src, 'rb') as f:
            fdata = f.read()
        result['local_filesize'] = filesize
    except Exception as e:
        result['failed'] = True
        result['msg'] = ('Unable to read src file: %s' % str(e))
        return result
    file_attribute = vim.vm.guest.FileManager.FileAttributes()
    url = self.content.guestOperationsManager.fileManager.InitiateFileTransferToGuest(vm, creds, dest, file_attribute, filesize, overwrite)
    (rsp, info) = fetch_url(self.module, url, method='put', data=fdata, use_proxy=False, force=True, last_mod_time=None, timeout=10, headers=None)
    result['msg'] = str(rsp.read())
    for (k, v) in info.items():
        result[k] = v
    return result