

def _populate_from_source(self, source_data, using_current_cache):
    '\n        Populate inventory data from direct source\n\n        '
    if using_current_cache:
        self._populate_from_cache(source_data)
        return source_data
    cacheable_results = {
        '_meta': {
            'hostvars': {
                
            },
        },
    }
    hostvars = {
        
    }
    objects = self.pyv._get_managed_objects_properties(vim_type=vim.VirtualMachine, properties=['name'])
    if self.pyv.with_tags:
        tag_svc = Tag(self.pyv.rest_content)
        tag_association = TagAssociation(self.pyv.rest_content)
        tags_info = dict()
        tags = tag_svc.list()
        for tag in tags:
            tag_obj = tag_svc.get(tag)
            tags_info[tag_obj.id] = tag_obj.name
            if (tag_obj.name not in cacheable_results):
                cacheable_results[tag_obj.name] = {
                    'hosts': [],
                }
                self.inventory.add_group(tag_obj.name)
    for vm_obj in objects:
        for vm_obj_property in vm_obj.propSet:
            current_host = ((vm_obj_property.val + '_') + vm_obj.obj.config.uuid)
            if (current_host not in hostvars):
                hostvars[current_host] = {
                    
                }
                self.inventory.add_host(current_host)
                host_ip = vm_obj.obj.guest.ipAddress
                if host_ip:
                    self.inventory.set_variable(current_host, 'ansible_host', host_ip)
                self._populate_host_properties(vm_obj, current_host)
                if (HAS_VCLOUD and HAS_VSPHERE and self.pyv.with_tags):
                    vm_mo_id = vm_obj.obj._GetMoId()
                    vm_dynamic_id = DynamicID(type='VirtualMachine', id=vm_mo_id)
                    attached_tags = tag_association.list_attached_tags(vm_dynamic_id)
                    for tag_id in attached_tags:
                        self.inventory.add_child(tags_info[tag_id], current_host)
                        cacheable_results[tags_info[tag_id]]['hosts'].append(current_host)
                vm_power = str(vm_obj.obj.summary.runtime.powerState)
                if (vm_power not in cacheable_results):
                    cacheable_results[vm_power] = {
                        'hosts': [],
                    }
                    self.inventory.add_group(vm_power)
                cacheable_results[vm_power]['hosts'].append(current_host)
                self.inventory.add_child(vm_power, current_host)
                vm_guest_id = vm_obj.obj.config.guestId
                if (vm_guest_id and (vm_guest_id not in cacheable_results)):
                    cacheable_results[vm_guest_id] = {
                        'hosts': [],
                    }
                    self.inventory.add_group(vm_guest_id)
                cacheable_results[vm_guest_id]['hosts'].append(current_host)
                self.inventory.add_child(vm_guest_id, current_host)
    for host in hostvars:
        h = self.inventory.get_host(host)
        cacheable_results['_meta']['hostvars'][h.name] = h.vars
    return cacheable_results
