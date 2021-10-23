

def main():
    global module, units_si, units_iec, parted_exec
    changed = False
    output_script = ''
    script = ''
    module = AnsibleModule(argument_spec={
        'device': {
            'required': True,
            'type': 'str',
        },
        'align': {
            'default': 'optimal',
            'choices': ['none', 'cylinder', 'minimal', 'optimal'],
            'type': 'str',
        },
        'number': {
            'default': None,
            'type': 'int',
        },
        'unit': {
            'default': 'KiB',
            'choices': parted_units,
            'type': 'str',
        },
        'label': {
            'choices': ['aix', 'amiga', 'bsd', 'dvh', 'gpt', 'loop', 'mac', 'msdos', 'pc98', 'sun'],
            'type': 'str',
        },
        'part_type': {
            'default': 'primary',
            'choices': ['primary', 'extended', 'logical'],
            'type': 'str',
        },
        'part_start': {
            'default': '0%',
            'type': 'str',
        },
        'part_end': {
            'default': '100%',
            'type': 'str',
        },
        'name': {
            'type': 'str',
        },
        'flags': {
            'type': 'list',
        },
        'state': {
            'choices': ['present', 'absent', 'info'],
            'default': 'info',
            'type': 'str',
        },
    }, supports_check_mode=True)
    device = module.params['device']
    align = module.params['align']
    number = module.params['number']
    unit = module.params['unit']
    label = module.params['label']
    part_type = module.params['part_type']
    part_start = module.params['part_start']
    part_end = module.params['part_end']
    name = module.params['name']
    state = module.params['state']
    flags = module.params['flags']
    parted_exec = module.get_bin_path('parted', True)
    if (number and (number < 0)):
        module.fail_json(msg='The partition number must be non negative.')
    if (not check_size_format(part_start)):
        module.fail_json(msg="The argument 'part_start' doesn't respect required format.The size unit is case sensitive.", err=parse_unit(part_start))
    if (not check_size_format(part_end)):
        module.fail_json(msg="The argument 'part_end' doesn't respect required format.The size unit is case sensitive.", err=parse_unit(part_end))
    current_device = get_device_info(device, unit)
    current_parts = current_device['partitions']
    if (state == 'present'):
        if (not label):
            label = 'msdos'
        if (current_device['generic'].get('table', None) != label):
            script += ('mklabel %s ' % label)
        if (part_type and (not part_exists(current_parts, 'num', number))):
            script += ('mkpart %s %s %s ' % (part_type, part_start, part_end))
        if (unit and script):
            script = ('unit %s %s' % (unit, script))
        if script:
            output_script += script
            parted(script, device, align)
            changed = True
            script = ''
            current_parts = get_device_info(device, unit)['partitions']
        if (part_exists(current_parts, 'num', number) or module.check_mode):
            partition = {
                'flags': [],
            }
            if (not module.check_mode):
                partition = [p for p in current_parts if (p['num'] == number)][0]
            if ((name is not None) and (partition.get('name', None) != name)):
                script += ('name %s %s ' % (number, name))
            if flags:
                flags_off = list((set(partition['flags']) - set(flags)))
                flags_on = list((set(flags) - set(partition['flags'])))
                for f in flags_on:
                    script += ('set %s %s on ' % (number, f))
                for f in flags_off:
                    script += ('set %s %s off ' % (number, f))
        if (unit and script):
            script = ('unit %s %s' % (unit, script))
        if script:
            output_script += script
            changed = True
            parted(script, device, align)
    elif (state == 'absent'):
        if (part_exists(current_parts, 'num', number) or module.check_mode):
            script = ('rm %s ' % number)
            output_script += script
            changed = True
            parted(script, device, align)
    elif (state == 'info'):
        output_script = ("unit '%s' print " % unit)
    final_device_status = get_device_info(device, unit)
    module.exit_json(changed=changed, disk=final_device_status['generic'], partitions=final_device_status['partitions'], script=output_script.strip())
