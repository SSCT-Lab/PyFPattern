def get_nfs_service(self):
    '\n        Return details about nfs\n        :param:\n            name : name of the vserver\n        :return: Details about nfs. None if not found.\n        :rtype: dict\n        '
    nfs_get_iter = netapp_utils.zapi.NaElement('nfs-service-get-iter')
    nfs_info = netapp_utils.zapi.NaElement('nfs-info')
    nfs_info.add_new_child('vserver', self.vserver)
    query = netapp_utils.zapi.NaElement('query')
    query.add_child_elem(nfs_info)
    nfs_get_iter.add_child_elem(query)
    result = self.server.invoke_successfully(nfs_get_iter, True)
    nfs_details = None
    if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) >= 1)):
        attributes_list = result.get_child_by_name('attributes-list').get_child_by_name('nfs-info')
        is_nfsv3_enabled = attributes_list.get_child_content('is-nfsv3-enabled')
        is_nfsv3_fsid_change_enabled = attributes_list.get_child_content('is-nfsv3-fsid-change-enabled')
        is_nfsv40_enabled = attributes_list.get_child_content('is-nfsv40-enabled')
        is_nfsv41_enabled = attributes_list.get_child_content('is-nfsv41-enabled')
        is_vstorage_enabled = attributes_list.get_child_content('is-vstorage-enabled')
        nfsv4_id_domain_value = attributes_list.get_child_content('nfsv4-id-domain')
        is_tcp_enabled = attributes_list.get_child_content('is-tcp-enabled')
        is_udp_enabled = attributes_list.get_child_content('is-udp-enabled')
        is_nfsv40_acl_enabled = attributes_list.get_child_content('is-nfsv40-acl-enabled')
        is_nfsv40_write_delegation_enabled = attributes_list.get_child_content('is-nfsv40-write-delegation-enabled')
        is_nfsv40_read_delegation_enabled = attributes_list.get_child_content('is-nfsv40-read-delegation-enabled')
        is_nfsv41_acl_enabled = attributes_list.get_child_content('is-nfsv41-acl-enabled')
        is_nfsv41_write_delegation_enabled = attributes_list.get_child_content('is-nfsv41-write-delegation-enabled')
        is_nfsv41_read_delegation_enabled = attributes_list.get_child_content('is-nfsv41-read-delegation-enabled')
        is_showmount_enabled = attributes_list.get_child_content('showmount')
        nfs_details = {
            'is_nfsv3_enabled': is_nfsv3_enabled,
            'is_nfsv3_fsid_change_enabled': is_nfsv3_fsid_change_enabled,
            'is_nfsv40_enabled': is_nfsv40_enabled,
            'is_nfsv41_enabled': is_nfsv41_enabled,
            'is_vstorage_enabled': is_vstorage_enabled,
            'nfsv4_id_domain': nfsv4_id_domain_value,
            'is_tcp_enabled': is_tcp_enabled,
            'is_udp_enabled': is_udp_enabled,
            'is_nfsv40_acl_enabled': is_nfsv40_acl_enabled,
            'is_nfsv40_write_delegation_enabled': is_nfsv40_write_delegation_enabled,
            'is_nfsv40_read_delegation_enabled': is_nfsv40_read_delegation_enabled,
            'is_nfsv41_acl_enabled': is_nfsv41_acl_enabled,
            'is_nfsv41_write_delegation_enabled': is_nfsv41_write_delegation_enabled,
            'is_nfsv41_read_delegation_enabled': is_nfsv41_read_delegation_enabled,
            'is_showmount_enabled': is_showmount_enabled,
        }
    return nfs_details