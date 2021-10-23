def select_datastore(self, vm_obj=None):
    datastore = None
    datastore_name = None
    if (len(self.params['disk']) != 0):
        if (('autoselect_datastore' in self.params['disk'][0]) and self.params['disk'][0]['autoselect_datastore']):
            datastores = get_all_objs(self.content, [vim.Datastore])
            if ((datastores is None) or (len(datastores) == 0)):
                self.module.fail_json(msg='Unable to find a datastore list when autoselecting')
            datastore_freespace = 0
            for ds in datastores:
                if (ds.summary.freeSpace > datastore_freespace):
                    if (('datastore' in self.params['disk'][0]) and isinstance(self.params['disk'][0]['datastore'], str) and (ds.name.find(self.params['disk'][0]['datastore']) < 0)):
                        continue
                    datastore = ds
                    datastore_name = datastore.name
                    datastore_freespace = ds.summary.freeSpace
        elif ('datastore' in self.params['disk'][0]):
            datastore_name = self.params['disk'][0]['datastore']
            datastore = get_obj(self.content, [vim.Datastore], datastore_name)
        else:
            self.module.fail_json(msg='Either datastore or autoselect_datastore should be provided to select datastore')
    if ((not datastore) and self.should_deploy_from_template()):
        disks = [x for x in vm_obj.config.hardware.device if isinstance(x, vim.vm.device.VirtualDisk)]
        datastore = disks[0].backing.datastore
        datastore_name = datastore.name
    if (not datastore):
        self.module.fail_json(msg='Failed to find a matching datastore')
    return (datastore, datastore_name)