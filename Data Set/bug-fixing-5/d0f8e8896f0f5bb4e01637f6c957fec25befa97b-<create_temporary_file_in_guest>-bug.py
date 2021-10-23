def create_temporary_file_in_guest(self, prefix='', suffix=''):
    'Create a temporary file in the VM.'
    try:
        return self.fileManager.CreateTemporaryFileInGuest(vm=self.vm, auth=self.vm_auth, prefix=prefix, suffix=suffix)
    except vim.fault.NoPermission as e:
        raise AnsibleError(('No Permission Error: %s %s' % (to_native(e.msg), to_native(e.privilegeId))))