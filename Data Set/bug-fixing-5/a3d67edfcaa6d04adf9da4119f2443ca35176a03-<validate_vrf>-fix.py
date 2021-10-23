def validate_vrf(name, module):
    if name:
        name = name.strip()
        if (name == 'default'):
            module.fail_json(msg='cannot use default as name of a VRF')
        elif (len(name) > 32):
            module.fail_json(msg='VRF name exceeded max length of 32', name=name)
        else:
            return name