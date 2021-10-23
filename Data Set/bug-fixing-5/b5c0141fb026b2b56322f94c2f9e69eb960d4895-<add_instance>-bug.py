def add_instance(self, instance, region):
    ' Adds an instance to the inventory and index, as long as it is\n        addressable '
    if (instance.state not in self.ec2_instance_states):
        return
    if (self.destination_format and self.destination_format_tags):
        dest_vars = []
        inst_tags = getattr(instance, 'tags')
        for tag in self.destination_format_tags:
            if (tag in inst_tags):
                dest_vars.append(inst_tags[tag])
            elif hasattr(instance, tag):
                dest_vars.append(getattr(instance, tag))
            else:
                dest_vars.append('nil')
        dest = self.destination_format.format(*dest_vars)
    elif instance.subnet_id:
        dest = getattr(instance, self.vpc_destination_variable, None)
        if (dest is None):
            dest = getattr(instance, 'tags').get(self.vpc_destination_variable, None)
    else:
        dest = getattr(instance, self.destination_variable, None)
        if (dest is None):
            dest = getattr(instance, 'tags').get(self.destination_variable, None)
    if (not dest):
        return
    hostname = None
    if self.hostname_variable:
        if self.hostname_variable.startswith('tag_'):
            hostname = instance.tags.get(self.hostname_variable[4:], None)
        else:
            hostname = getattr(instance, self.hostname_variable)
    if (self.route53_enabled and self.route53_hostnames):
        route53_names = self.get_instance_route53_names(instance)
        for name in route53_names:
            if name.endswith(self.route53_hostnames):
                hostname = name
    if (not hostname):
        hostname = dest
    elif (self.route53_enabled and self.route53_hostnames and hostname.endswith(self.route53_hostnames)):
        hostname = hostname.lower()
    else:
        hostname = self.to_safe(hostname).lower()
    if (self.pattern_include and (not self.pattern_include.match(hostname))):
        return
    if (self.pattern_exclude and self.pattern_exclude.match(hostname)):
        return
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
        self.push(self.inventory, instance.placement, hostname)
        if self.nested_groups:
            if self.group_by_region:
                self.push_group(self.inventory, region, instance.placement)
            self.push_group(self.inventory, 'zones', instance.placement)
    if self.group_by_ami_id:
        ami_id = self.to_safe(instance.image_id)
        self.push(self.inventory, ami_id, hostname)
        if self.nested_groups:
            self.push_group(self.inventory, 'images', ami_id)
    if self.group_by_instance_type:
        type_name = self.to_safe(('type_' + instance.instance_type))
        self.push(self.inventory, type_name, hostname)
        if self.nested_groups:
            self.push_group(self.inventory, 'types', type_name)
    if self.group_by_instance_state:
        state_name = self.to_safe(('instance_state_' + instance.state))
        self.push(self.inventory, state_name, hostname)
        if self.nested_groups:
            self.push_group(self.inventory, 'instance_states', state_name)
    if self.group_by_platform:
        if instance.platform:
            platform = self.to_safe(('platform_' + instance.platform))
        else:
            platform = self.to_safe('platform_undefined')
        self.push(self.inventory, platform, hostname)
        if self.nested_groups:
            self.push_group(self.inventory, 'platforms', platform)
    if (self.group_by_key_pair and instance.key_name):
        key_name = self.to_safe(('key_' + instance.key_name))
        self.push(self.inventory, key_name, hostname)
        if self.nested_groups:
            self.push_group(self.inventory, 'keys', key_name)
    if (self.group_by_vpc_id and instance.vpc_id):
        vpc_id_name = self.to_safe(('vpc_id_' + instance.vpc_id))
        self.push(self.inventory, vpc_id_name, hostname)
        if self.nested_groups:
            self.push_group(self.inventory, 'vpcs', vpc_id_name)
    if self.group_by_security_group:
        try:
            for group in instance.groups:
                key = self.to_safe(('security_group_' + group.name))
                self.push(self.inventory, key, hostname)
                if self.nested_groups:
                    self.push_group(self.inventory, 'security_groups', key)
        except AttributeError:
            self.fail_with_error('\n'.join(['Package boto seems a bit older.', 'Please upgrade boto >= 2.3.0.']))
    if self.group_by_aws_account:
        self.push(self.inventory, self.aws_account_id, dest)
        if self.nested_groups:
            self.push_group(self.inventory, 'accounts', self.aws_account_id)
    if self.group_by_tag_keys:
        for (k, v) in instance.tags.items():
            if (self.expand_csv_tags and v and (',' in v)):
                values = map((lambda x: x.strip()), v.split(','))
            else:
                values = [v]
            for v in values:
                if v:
                    key = self.to_safe(((('tag_' + k) + '=') + v))
                else:
                    key = self.to_safe(('tag_' + k))
                self.push(self.inventory, key, hostname)
                if self.nested_groups:
                    self.push_group(self.inventory, 'tags', self.to_safe(('tag_' + k)))
                    if v:
                        self.push_group(self.inventory, self.to_safe(('tag_' + k)), key)
    if (self.route53_enabled and self.group_by_route53_names):
        route53_names = self.get_instance_route53_names(instance)
        for name in route53_names:
            self.push(self.inventory, name, hostname)
            if self.nested_groups:
                self.push_group(self.inventory, 'route53', name)
    if (self.group_by_tag_none and (len(instance.tags) == 0)):
        self.push(self.inventory, 'tag_none', hostname)
        if self.nested_groups:
            self.push_group(self.inventory, 'tags', 'tag_none')
    self.push(self.inventory, 'ec2', hostname)
    self.inventory['_meta']['hostvars'][hostname] = self.get_host_info_dict_from_instance(instance)
    self.inventory['_meta']['hostvars'][hostname]['ansible_host'] = dest