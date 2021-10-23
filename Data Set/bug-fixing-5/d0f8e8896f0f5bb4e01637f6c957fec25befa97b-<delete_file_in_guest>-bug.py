def delete_file_in_guest(self, filePath):
    'Delete file from VM.'
    try:
        self.fileManager.DeleteFileInGuest(vm=self.vm, auth=self.vm_auth, filePath=filePath)
    except vim.fault.NoPermission as e:
        raise AnsibleError(('No Permission Error: %s %s' % (to_native(e.msg), to_native(e.privilegeId))))