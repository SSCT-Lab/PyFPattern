def get_host_info(self):
    '\n        Get variables about a specific host\n        '
    if (len(self.index) == 0):
        self.load_index_from_cache()
    if (self.args.host not in self.index):
        self.do_api_calls_update_cache()
        if (self.args.host not in self.index):
            return self.json_format_dict({
                
            }, True)
    node_id = self.index[self.args.host]
    node = self.get_node(node_id)
    instance_vars = {
        
    }
    for key in vars(instance):
        value = getattr(instance, key)
        key = self.to_safe(('ec2_' + key))
        if isinstance(value, (int, bool)):
            instance_vars[key] = value
        elif isinstance(value, string_types):
            instance_vars[key] = value.strip()
        elif (value is None):
            instance_vars[key] = ''
        elif (key == 'ec2_region'):
            instance_vars[key] = value.name
        elif (key == 'ec2_tags'):
            for (k, v) in iteritems(value):
                key = self.to_safe(('ec2_tag_' + k))
                instance_vars[key] = v
        elif (key == 'ec2_groups'):
            group_ids = []
            group_names = []
            for group in value:
                group_ids.append(group.id)
                group_names.append(group.name)
            instance_vars['ec2_security_group_ids'] = ','.join(group_ids)
            instance_vars['ec2_security_group_names'] = ','.join(group_names)
        else:
            pass
    return self.json_format_dict(instance_vars, True)