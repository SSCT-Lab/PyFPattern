def add_rds_instance(self, instance, region):
    ' Adds an RDS instance to the inventory and index, as long as it is\n        addressable '
    if ((not self.all_rds_instances) and (instance.status != 'available')):
        return
    dest = instance.endpoint[0]
    if (not dest):
        return
    hostname = None
    if self.hostname_variable:
        if self.hostname_variable.startswith('tag_'):
            hostname = instance.tags.get(self.hostname_variable[4:], None)
        else:
            hostname = getattr(instance, self.hostname_variable)
    if (not hostname):
        hostname = dest
    hostname = self.to_safe(hostname).lower()
    self.index[hostname] = [region, instance.id]
    if self.group_by_instance_id:
        self.inventory[instance.id] = [hostname]
        if self.nested_groups:
            self.push_group(self.inventory, 'instances', instance.id)
    if self.group_by_region:
        self.push(self.inventory, region, hostname)
        if self.nested_groups:
            self.push_group(self.inventory, 'regions', region)
    if self.group_by_availability_zone:
        self.push(self.inventory, instance.availability_zone, hostname)
        if self.nested_groups:
            if self.group_by_region:
                self.push_group(self.inventory, region, instance.availability_zone)
            self.push_group(self.inventory, 'zones', instance.availability_zone)
    if self.group_by_instance_type:
        type_name = self.to_safe(('type_' + instance.instance_class))
        self.push(self.inventory, type_name, hostname)
        if self.nested_groups:
            self.push_group(self.inventory, 'types', type_name)
    if (self.group_by_vpc_id and instance.subnet_group and instance.subnet_group.vpc_id):
        vpc_id_name = self.to_safe(('vpc_id_' + instance.subnet_group.vpc_id))
        self.push(self.inventory, vpc_id_name, hostname)
        if self.nested_groups:
            self.push_group(self.inventory, 'vpcs', vpc_id_name)
    if self.group_by_security_group:
        try:
            if instance.security_group:
                key = self.to_safe(('security_group_' + instance.security_group.name))
                self.push(self.inventory, key, hostname)
                if self.nested_groups:
                    self.push_group(self.inventory, 'security_groups', key)
        except AttributeError:
            self.fail_with_error('\n'.join(['Package boto seems a bit older.', 'Please upgrade boto >= 2.3.0.']))
    if self.group_by_rds_engine:
        self.push(self.inventory, self.to_safe(('rds_' + instance.engine)), hostname)
        if self.nested_groups:
            self.push_group(self.inventory, 'rds_engines', self.to_safe(('rds_' + instance.engine)))
    if self.group_by_rds_parameter_group:
        self.push(self.inventory, self.to_safe(('rds_parameter_group_' + instance.parameter_group.name)), hostname)
        if self.nested_groups:
            self.push_group(self.inventory, 'rds_parameter_groups', self.to_safe(('rds_parameter_group_' + instance.parameter_group.name)))
    self.push(self.inventory, 'rds', hostname)
    self.inventory['_meta']['hostvars'][hostname] = self.get_host_info_dict_from_instance(instance)
    self.inventory['_meta']['hostvars'][hostname]['ansible_ssh_host'] = dest