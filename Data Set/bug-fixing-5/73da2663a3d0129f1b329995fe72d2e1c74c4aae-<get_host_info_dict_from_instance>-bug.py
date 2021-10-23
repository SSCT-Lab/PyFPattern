def get_host_info_dict_from_instance(self, instance):
    instance_vars = {
        
    }
    for key in vars(instance):
        value = getattr(instance, key)
        key = self.to_safe(('ec2_' + key))
        if (key == 'ec2__state'):
            instance_vars['ec2_state'] = (instance.state or '')
            instance_vars['ec2_state_code'] = instance.state_code
        elif (key == 'ec2__previous_state'):
            instance_vars['ec2_previous_state'] = (instance.previous_state or '')
            instance_vars['ec2_previous_state_code'] = instance.previous_state_code
        elif (type(value) in [int, bool]):
            instance_vars[key] = value
        elif isinstance(value, six.string_types):
            instance_vars[key] = value.strip()
        elif (type(value) == type(None)):
            instance_vars[key] = ''
        elif (key == 'ec2_region'):
            instance_vars[key] = value.name
        elif (key == 'ec2__placement'):
            instance_vars['ec2_placement'] = value.zone
        elif (key == 'ec2_tags'):
            for (k, v) in value.items():
                if (self.expand_csv_tags and (',' in v)):
                    v = map((lambda x: x.strip()), v.split(','))
                key = self.to_safe(('ec2_tag_' + k))
                instance_vars[key] = v
        elif (key == 'ec2_groups'):
            group_ids = []
            group_names = []
            for group in value:
                group_ids.append(group.id)
                group_names.append(group.name)
            instance_vars['ec2_security_group_ids'] = ','.join([str(i) for i in group_ids])
            instance_vars['ec2_security_group_names'] = ','.join([str(i) for i in group_names])
        elif (key == 'ec2_block_device_mapping'):
            instance_vars['ec2_block_devices'] = {
                
            }
            for (k, v) in value.items():
                instance_vars['ec2_block_devices'][os.path.basename(k)] = v.volume_id
        else:
            pass
    return instance_vars