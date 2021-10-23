def apply(self):
    'Apply action to nfs'
    changed = False
    nfs_exists = False
    modify_nfs = False
    enable_nfs = False
    disable_nfs = False
    netapp_utils.ems_log_event('na_ontap_nfs', self.server)
    nfs_enabled = self.get_nfs_status()
    nfs_service_details = self.get_nfs_service()
    is_nfsv4_id_domain_changed = False

    def state_changed(expected, current):
        if ((expected == 'enabled') and (current == 'true')):
            return False
        if ((expected == 'disabled') and (current == 'false')):
            return False
        return True

    def is_modify_needed():
        if (((self.nfsv3 is not None) and state_changed(self.nfsv3, nfs_service_details['is_nfsv3_enabled'])) or ((self.nfsv4 is not None) and state_changed(self.nfsv4, nfs_service_details['is_nfsv40_enabled'])) or ((self.nfsv41 is not None) and state_changed(self.nfsv41, nfs_service_details['is_nfsv41_enabled'])) or ((self.tcp is not None) and state_changed(self.tcp, nfs_service_details['is_tcp_enabled'])) or ((self.udp is not None) and state_changed(self.udp, nfs_service_details['is_udp_enabled'])) or ((self.vstorage_state is not None) and state_changed(self.vstorage_state, nfs_service_details['is_vstorage_enabled']))):
            return True
        return False

    def is_domain_changed():
        if ((self.nfsv4_id_domain is not None) and (self.nfsv4_id_domain != nfs_service_details['nfsv4_id_domain'])):
            return True
        return False
    if nfs_service_details:
        nfs_exists = True
        if (self.state == 'absent'):
            changed = True
        elif (self.state == 'present'):
            if ((self.service_state == 'started') and (nfs_enabled == 'false')):
                enable_nfs = True
                changed = True
            elif ((self.service_state == 'stopped') and (nfs_enabled == 'true')):
                disable_nfs = True
                changed = True
            if is_modify_needed():
                modify_nfs = True
                changed = True
            if is_domain_changed():
                is_nfsv4_id_domain_changed = True
                changed = True
    elif (self.state == 'present'):
        changed = True
    if changed:
        if self.module.check_mode:
            pass
        elif (self.state == 'present'):
            if (not nfs_exists):
                self.enable_nfs()
                nfs_service_details = self.get_nfs_service()
                if (self.service_state == 'stopped'):
                    self.disable_nfs()
                if is_modify_needed():
                    self.modify_nfs()
                if is_domain_changed():
                    self.modify_nfsv4_id_domain()
            else:
                if enable_nfs:
                    self.enable_nfs()
                elif disable_nfs:
                    self.disable_nfs()
                if modify_nfs:
                    self.modify_nfs()
                if is_nfsv4_id_domain_changed:
                    self.modify_nfsv4_id_domain()
        elif (self.state == 'absent'):
            self.delete_nfs()
    self.module.exit_json(changed=changed)