def exec_module(self, **kwargs):
    for key in (list(self.module_arg_spec.keys()) + ['tags']):
        setattr(self, key, kwargs[key])
    results = None
    changed = False
    image = None
    if (not self.location):
        resource_group = self.get_resource_group(self.resource_group)
        self.location = resource_group.location
    self.log('Fetching image {0}'.format(self.name))
    image = self.get_image()
    if image:
        self.check_provisioning_state(image, self.state)
        results = image.id
        (update_tags, tags) = self.update_tags(image.tags)
        if update_tags:
            changed = True
            self.tags = tags
        if (self.state == 'absent'):
            changed = True
    elif (self.state == 'present'):
        changed = True
    self.results['changed'] = changed
    self.results['id'] = results
    if changed:
        if (self.state == 'present'):
            image_instance = None
            vm = self.get_source_vm()
            if vm:
                if self.data_disk_sources:
                    self.fail('data_disk_sources is not allowed when capturing image from vm')
                image_instance = self.compute_models.Image(self.location, source_virtual_machine=self.compute_models.SubResource(vm.id))
            else:
                if (not self.os_type):
                    self.fail('os_type is required to create the image')
                os_disk = self.create_os_disk()
                data_disks = self.create_data_disks()
                storage_profile = self.compute_models.ImageStorageProfile(os_disk=os_disk, data_disks=data_disks)
                image_instance = self.compute_models.Image(self.location, storage_profile=storage_profile, tags=self.tags)
            if ((not self.check_mode) and image_instance):
                new_image = self.create_image(image_instance)
                self.results['id'] = new_image.id
        elif (self.state == 'absent'):
            if (not self.check_mode):
                self.delete_image()
                self.results['id'] = None
    return self.results