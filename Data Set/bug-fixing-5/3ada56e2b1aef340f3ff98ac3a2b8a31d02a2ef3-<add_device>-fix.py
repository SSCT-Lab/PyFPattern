def add_device(self, device, project):
    ' Adds a device to the inventory and index, as long as it is\n        addressable '
    if (device.state not in self.packet_device_states):
        return
    dest = None
    for ip_address in device.ip_addresses:
        if ((ip_address['public'] is True) and (ip_address['address_family'] == 4) and (ip_address['management'] is True)):
            dest = ip_address['address']
    if (not dest):
        return
    if (self.pattern_include and (not self.pattern_include.match(device.hostname))):
        return
    if (self.pattern_exclude and self.pattern_exclude.match(device.hostname)):
        return
    self.index[dest] = [project.id, device.id]
    if self.group_by_device_id:
        self.inventory[device.id] = [dest]
        if self.nested_groups:
            self.push_group(self.inventory, 'devices', device.id)
    if self.group_by_hostname:
        self.push(self.inventory, device.hostname, dest)
        if self.nested_groups:
            self.push_group(self.inventory, 'hostnames', project.name)
    if self.group_by_project:
        self.push(self.inventory, project.name, dest)
        if self.nested_groups:
            self.push_group(self.inventory, 'projects', project.name)
    if self.group_by_facility:
        self.push(self.inventory, device.facility['code'], dest)
        if self.nested_groups:
            if self.group_by_facility:
                self.push_group(self.inventory, project.name, device.facility['code'])
    if self.group_by_operating_system:
        self.push(self.inventory, device.operating_system.slug, dest)
        if self.nested_groups:
            self.push_group(self.inventory, 'operating_systems', device.operating_system.slug)
    if self.group_by_plan_type:
        self.push(self.inventory, device.plan['slug'], dest)
        if self.nested_groups:
            self.push_group(self.inventory, 'plans', device.plan['slug'])
    if self.group_by_tags:
        for k in device.tags:
            key = self.to_safe(('tag_' + k))
            self.push(self.inventory, key, dest)
            if self.nested_groups:
                self.push_group(self.inventory, 'tags', self.to_safe(('tag_' + k)))
    if (self.group_by_tag_none and (len(device.tags) == 0)):
        self.push(self.inventory, 'tag_none', dest)
        if self.nested_groups:
            self.push_group(self.inventory, 'tags', 'tag_none')
    self.push(self.inventory, 'packet', dest)
    self.inventory['_meta']['hostvars'][dest] = self.get_host_info_dict_from_device(device)