def delete_file_in_guest(self, filePath):
    'Delete file from VM.'
    try:
        self.fileManager.DeleteFileInGuest(vm=self.vm, auth=self.vm_auth, filePath=filePath)
    except vim.fault.NoPermission as e:
        raise AnsibleError(('No Permission Error: %s %s' % (to_native(e.msg), to_native(e.privilegeId))))
    except vmodl.fault.SystemError as e:
        if (e.reason == 'vix error codes = (3016, 0).\n'):
            raise AnsibleConnectionFailure(('Connection failed, is the vm currently rebooting? Reason: %s' % to_native(e.reason)))
        else:
            raise AnsibleConnectionFailure(('Connection failed. Reason %s' % to_native(e.reason)))
    except vim.fault.GuestOperationsUnavailable:
        raise AnsibleConnectionFailure('Cannot connect to guest. Native error: GuestOperationsUnavailable')