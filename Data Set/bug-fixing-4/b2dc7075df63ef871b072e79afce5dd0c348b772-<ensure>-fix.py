def ensure(self):
    '\n        Manage internal state management\n        '
    state = self.module.params.get('state')
    folder_type = self.module.params.get('folder_type')
    folder_name = self.module.params.get('folder_name')
    parent_folder = self.module.params.get('parent_folder', None)
    results = dict(changed=False, result=dict())
    if (state == 'present'):
        p_folder_obj = None
        if parent_folder:
            p_folder_obj = self.get_folder(folder_name=parent_folder, folder_type=folder_type)
            if (not p_folder_obj):
                self.module.fail_json(msg=('Parent folder %s does not exist' % parent_folder))
            child_folder_obj = self.get_folder(folder_name=folder_name, folder_type=folder_type, parent_folder=p_folder_obj)
            if child_folder_obj:
                results['result'] = ('Folder %s already exists under parent folder %s' % (folder_name, parent_folder))
                self.module.exit_json(**results)
        else:
            folder_obj = self.get_folder(folder_name=folder_name, folder_type=folder_type)
            if folder_obj:
                results['result'] = ('Folder %s already exists' % folder_name)
                self.module.exit_json(**results)
        try:
            if (parent_folder and p_folder_obj):
                p_folder_obj.CreateFolder(folder_name)
                results['changed'] = True
                results['result'] = ("Folder '%s' of type '%s' created under %s successfully." % (folder_name, folder_type, parent_folder))
            elif ((not parent_folder) and (not p_folder_obj)):
                self.datacenter_folder_type[folder_type].CreateFolder(folder_name)
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
        folder_obj = self.get_folder(folder_name=folder_name, folder_type=folder_type)
        if folder_obj:
            try:
                task = folder_obj.UnregisterAndDestroy()
                (results['changed'], results['result']) = wait_for_task(task=task)
            except vim.fault.ConcurrentAccess as concurrent_access:
                self.module.fail_json(msg=('Failed to remove folder as another client modified folder before this operation : %s' % to_native(concurrent_access.msg)))
            except vim.fault.InvalidState as invalid_state:
                self.module.fail_json(msg=('Failed to remove folder as folder is in invalid state : %s' % to_native(invalid_state.msg)))
            except Exception as gen_exec:
                self.module.fail_json(msg=('Failed to remove folder due to generic exception %s ' % to_native(gen_exec)))
        self.module.exit_json(**results)