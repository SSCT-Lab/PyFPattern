def ensure(self):
    '\n        Function to manage internal state management\n        Returns:\n\n        '
    state = self.module.params.get('state')
    folder_type = self.module.params.get('folder_type')
    folder_name = self.module.params.get('folder_name')
    parent_folder = self.module.params.get('parent_folder', None)
    results = dict(changed=False, result=dict())
    if (state == 'present'):
        try:
            if parent_folder:
                folder = self.get_folder_by_name(folder_name=parent_folder)
                if (folder and (not self.get_folder_by_name(folder_name=folder_name, parent_folder=folder))):
                    folder.CreateFolder(folder_name)
                    results['changed'] = True
                    results['result'] = ("Folder '%s' of type '%s' created under %s successfully." % (folder_name, folder_type, parent_folder))
                elif (folder is None):
                    self.module.fail_json(msg=('Failed to find the parent folder %s for folder %s' % (parent_folder, folder_name)))
            else:
                datacenter_folder_type = {
                    'vm': self.datacenter_obj.vmFolder,
                    'host': self.datacenter_obj.hostFolder,
                    'datastore': self.datacenter_obj.datastoreFolder,
                    'network': self.datacenter_obj.networkFolder,
                }
                datacenter_folder_type[folder_type].CreateFolder(folder_name)
                results['changed'] = True
                results['result'] = ("Folder '%s' of type '%s' created successfully" % (folder_name, folder_type))
        except vim.fault.DuplicateName as duplicate_name:
            results['changed'] = False
            results['result'] = ('Failed to create folder as another object has same name in the same target folder : %s' % to_native(duplicate_name.msg))
        except vim.fault.InvalidName as invalid_name:
            self.module.fail_json(msg=('Failed to create folder as folder name is not a valid entity name : %s' % to_native(invalid_name.msg)))
        except Exception as general_exc:
            self.module.fail_json(msg=('Failed to create folder due to generic exception : %s ' % to_native(general_exc)))
        self.module.exit_json(**results)
    elif (state == 'absent'):
        folder_obj = self.get_folder_by_name(folder_name=folder_name)
        if folder_obj:
            try:
                task = folder_obj.UnregisterAndDestroy()
                (results['changed'], results['result']) = wait_for_task(task=task)
            except vim.fault.ConcurrentAccess as concurrent_access:
                self.module.fail_json(msg=('Failed to remove folder as another client modified folder before this operation : %s' % to_native(concurrent_access.msg)))
            except vim.fault.InvalidState as invalid_state:
                self.module.fail_json(msg=('Failed to remove folder as folder is in invalid state' % to_native(invalid_state.msg)))
            except Exception as e:
                self.module.fail_json(msg=('Failed to remove folder due to generic exception %s ' % to_native(e)))
        self.module.exit_json(**results)