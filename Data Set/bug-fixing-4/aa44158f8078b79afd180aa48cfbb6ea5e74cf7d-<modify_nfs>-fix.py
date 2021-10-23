def modify_nfs(self):
    '\n        modify nfs service\n        '
    nfs_modify = netapp_utils.zapi.NaElement('nfs-service-modify')
    if (self.nfsv3 == 'enabled'):
        nfs_modify.add_new_child('is-nfsv3-enabled', 'true')
    elif (self.nfsv3 == 'disabled'):
        nfs_modify.add_new_child('is-nfsv3-enabled', 'false')
    if (self.nfsv3_fsid_change == 'enabled'):
        nfs_modify.add_new_child('is-nfsv3-fsid-change-enabled', 'true')
    elif (self.nfsv3_fsid_change == 'disabled'):
        nfs_modify.add_new_child('is-nfsv3-fsid-change-enabled', 'false')
    if (self.nfsv4 == 'enabled'):
        nfs_modify.add_new_child('is-nfsv40-enabled', 'true')
    elif (self.nfsv4 == 'disabled'):
        nfs_modify.add_new_child('is-nfsv40-enabled', 'false')
    if (self.nfsv41 == 'enabled'):
        nfs_modify.add_new_child('is-nfsv41-enabled', 'true')
    elif (self.nfsv41 == 'disabled'):
        nfs_modify.add_new_child('is-nfsv41-enabled', 'false')
    if (self.vstorage_state == 'enabled'):
        nfs_modify.add_new_child('is-vstorage-enabled', 'true')
    elif (self.vstorage_state == 'disabled'):
        nfs_modify.add_new_child('is-vstorage-enabled', 'false')
    if (self.tcp == 'enabled'):
        nfs_modify.add_new_child('is-tcp-enabled', 'true')
    elif (self.tcp == 'disabled'):
        nfs_modify.add_new_child('is-tcp-enabled', 'false')
    if (self.udp == 'enabled'):
        nfs_modify.add_new_child('is-udp-enabled', 'true')
    elif (self.udp == 'disabled'):
        nfs_modify.add_new_child('is-udp-enabled', 'false')
    if (self.nfsv40_acl == 'enabled'):
        nfs_modify.add_new_child('is-nfsv40-acl-enabled', 'true')
    elif (self.nfsv40_acl == 'disabled'):
        nfs_modify.add_new_child('is-nfsv40-acl-enabled', 'false')
    if (self.nfsv40_read_delegation == 'enabled'):
        nfs_modify.add_new_child('is-nfsv40-read-delegation-enabled', 'true')
    elif (self.nfsv40_read_delegation == 'disabled'):
        nfs_modify.add_new_child('is-nfsv40-read-delegation-enabled', 'false')
    if (self.nfsv40_write_delegation == 'enabled'):
        nfs_modify.add_new_child('is-nfsv40-write-delegation-enabled', 'true')
    elif (self.nfsv40_write_delegation == 'disabled'):
        nfs_modify.add_new_child('is-nfsv40-write-delegation-enabled', 'false')
    if (self.nfsv41_acl == 'enabled'):
        nfs_modify.add_new_child('is-nfsv41-acl-enabled', 'true')
    elif (self.nfsv41_acl == 'disabled'):
        nfs_modify.add_new_child('is-nfsv41-acl-enabled', 'false')
    if (self.nfsv41_read_delegation == 'enabled'):
        nfs_modify.add_new_child('is-nfsv41-read-delegation-enabled', 'true')
    elif (self.nfsv41_read_delegation == 'disabled'):
        nfs_modify.add_new_child('is-nfsv41-read-delegation-enabled', 'false')
    if (self.nfsv41_write_delegation == 'enabled'):
        nfs_modify.add_new_child('is-nfsv41-write-delegation-enabled', 'true')
    elif (self.nfsv41_write_delegation == 'disabled'):
        nfs_modify.add_new_child('is-nfsv41-write-delegation-enabled', 'false')
    if (self.showmount == 'enabled'):
        nfs_modify.add_new_child('showmount', 'true')
    elif (self.showmount == 'disabled'):
        nfs_modify.add_new_child('showmount', 'false')
    try:
        self.server.invoke_successfully(nfs_modify, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error modifying nfs: %s' % to_native(error)), exception=traceback.format_exc())