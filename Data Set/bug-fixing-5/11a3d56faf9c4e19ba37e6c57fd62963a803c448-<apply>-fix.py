def apply(self):
    changed = False
    vserver_details = self.get_vserver()
    rename_vserver = False
    modify_protocols = False
    modify_aggr_list = False
    modify_snapshot_policy = False
    modify_language = False
    if (vserver_details is not None):
        if (self.state == 'absent'):
            changed = True
        elif (self.state == 'present'):
            if (self.allowed_protocols is not None):
                self.allowed_protocols.sort()
                vserver_details['allowed_protocols'].sort()
                if (self.allowed_protocols != vserver_details['allowed_protocols']):
                    modify_protocols = True
                    changed = True
            if (self.aggr_list is not None):
                self.aggr_list.sort()
                vserver_details['aggr_list'].sort()
                if (self.aggr_list != vserver_details['aggr_list']):
                    modify_aggr_list = True
                    changed = True
            if (self.snapshot_policy is not None):
                if (self.snapshot_policy != vserver_details['snapshot_policy']):
                    modify_snapshot_policy = True
                    changed = True
            if (self.language is not None):
                if (self.language != vserver_details['language']):
                    modify_language = True
                    changed = True
            if ((self.root_volume is not None) and (self.root_volume != vserver_details['root_volume'])):
                self.module.fail_json(msg=('Error modifying SVM %s: %s' % (self.name, 'cannot change root volume')))
            if ((self.root_volume_aggregate is not None) and (self.root_volume_aggregate != vserver_details['root_volume_aggregate'])):
                self.module.fail_json(msg=('Error modifying SVM %s: %s' % (self.name, 'cannot change root volume aggregate')))
            if ((self.root_volume_security_style is not None) and (self.root_volume_security_style != vserver_details['root_volume_security_style'])):
                self.module.fail_json(msg=('Error modifying SVM %s: %s' % (self.name, 'cannot change root volume security style')))
            if ((self.subtype is not None) and (self.subtype != vserver_details['subtype'])):
                self.module.fail_json(msg=('Error modifying SVM %s: %s' % (self.name, 'cannot change subtype')))
            if ((self.ipspace is not None) and (self.ipspace != vserver_details['ipspace'])):
                self.module.fail_json(msg=('Error modifying SVM %s: %s' % (self.name, 'cannot change ipspace')))
    elif (self.state == 'present'):
        changed = True
    if changed:
        if self.module.check_mode:
            pass
        elif (self.state == 'present'):
            if (vserver_details is None):
                if ((self.from_name is not None) and self.get_vserver(self.from_name)):
                    self.rename_vserver()
                else:
                    self.create_vserver()
            elif (modify_protocols or modify_aggr_list):
                self.modify_vserver(modify_protocols, modify_aggr_list, modify_language, modify_snapshot_policy)
        elif (self.state == 'absent'):
            self.delete_vserver()
    self.module.exit_json(changed=changed)