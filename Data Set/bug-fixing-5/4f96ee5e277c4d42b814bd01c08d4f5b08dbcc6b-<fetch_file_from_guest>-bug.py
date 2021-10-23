def fetch_file_from_guest(content, vm, username, password, src, dest):
    " Use VMWare's filemanager api to fetch a file over http "
    result = {
        'failed': False,
    }
    tools_status = vm.guest.toolsStatus
    if ((tools_status == 'toolsNotInstalled') or (tools_status == 'toolsNotRunning')):
        result['failed'] = True
        result['msg'] = 'VMwareTools is not installed or is not running in the guest'
        return result
    creds = vim.vm.guest.NamePasswordAuthentication(username=username, password=password)
    fti = content.guestOperationsManager.fileManager.InitiateFileTransferFromGuest(vm, creds, src)
    result['size'] = fti.size
    result['url'] = fti.url
    (rsp, info) = fetch_url(self.module, fti.url, use_proxy=False, force=True, last_mod_time=None, timeout=10, headers=None)
    for (k, v) in iteritems(info):
        result[k] = v
    if (info['status'] != 200):
        result['failed'] = True
        return result
    try:
        with open(dest, 'wb') as f:
            f.write(rsp.read())
    except Exception as e:
        result['failed'] = True
        result['msg'] = str(e)
    return result