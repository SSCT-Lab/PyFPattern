def _establish_vm(self, check_vm_credentials=True):
    searchIndex = self._si.content.searchIndex
    self.vm = searchIndex.FindByInventoryPath(self.get_option('vm_path'))
    if (self.vm is None):
        raise AnsibleError(("Unable to find VM by path '%s'" % to_native(self.get_option('vm_path'))))
    self.vm_auth = vim.NamePasswordAuthentication(username=self.get_option('vm_user'), password=self.get_option('vm_password'), interactiveSession=False)
    try:
        if check_vm_credentials:
            self.authManager.ValidateCredentialsInGuest(vm=self.vm, auth=self.vm_auth)
    except vim.fault.InvalidPowerState as e:
        raise AnsibleError(('VM Power State Error: %s' % to_native(e.msg)))
    except vim.fault.RestrictedVersion as e:
        raise AnsibleError(('Restricted Version Error: %s' % to_native(e.msg)))
    except vim.fault.GuestOperationsUnavailable as e:
        raise AnsibleError(('VM Guest Operations (VMware Tools) Error: %s' % to_native(e.msg)))
    except vim.fault.InvalidGuestLogin as e:
        raise AnsibleError(('VM Login Error: %s' % to_native(e.msg)))
    except vim.fault.NoPermission as e:
        raise AnsibleConnectionFailure(('No Permission Error: %s %s' % (to_native(e.msg), to_native(e.privilegeId))))
    except vmodl.fault.SystemError as e:
        if (e.reason == 'vix error codes = (3016, 0).\n'):
            raise AnsibleConnectionFailure(('Connection failed, is the vm currently rebooting? Reason: %s' % to_native(e.reason)))
        else:
            raise AnsibleConnectionFailure(('Connection failed. Reason %s' % to_native(e.reason)))
    except vim.fault.GuestOperationsUnavailable:
        raise AnsibleConnectionFailure('Cannot connect to guest. Native error: GuestOperationsUnavailable')