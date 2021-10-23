def get_host_info_dict_from_device(self, device):
    device_vars = {
        
    }
    for key in vars(device):
        value = getattr(device, key)
        key = self.to_safe(('packet_' + key))
        if (key == 'packet_state'):
            device_vars[key] = (device.state or '')
        elif (key == 'packet_hostname'):
            device_vars[key] = value
        elif (type(value) in [int, bool]):
            device_vars[key] = value
        elif isinstance(value, six.string_types):
            device_vars[key] = value.strip()
        elif (value is None):
            device_vars[key] = ''
        elif (key == 'packet_facility'):
            device_vars[key] = value['code']
        elif (key == 'packet_operating_system'):
            device_vars[key] = value.slug
        elif (key == 'packet_plan'):
            device_vars[key] = value['slug']
        elif (key == 'packet_tags'):
            for k in value:
                key = self.to_safe(('packet_tag_' + k))
                device_vars[key] = k
        else:
            pass
    return device_vars