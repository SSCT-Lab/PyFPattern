def get_connection(vsys=None, device_group=None, vsys_dg=None, vsys_importable=None, rulebase=None, template=None, template_stack=None, with_classic_provider_spec=False, with_state=True, argument_spec=None, required_one_of=None, min_pandevice_version=None, min_panos_version=None, panorama_error=None, firewall_error=None):
    'Returns a helper object that handles pandevice object tree init.\n\n    The `vsys`, `device_group`, `vsys_dg`, `vsys_importable`, `rulebase`,\n    `template`, and `template_stack` params can be any of the following types:\n\n        * None - do not include this in the spec\n        * True - use the default param name\n        * string - use this string for the param name\n\n    The `min_pandevice_version` and `min_panos_version` args expect a 3 element\n    tuple of ints.  For example, `(0, 6, 0)` or `(8, 1, 0)`.\n\n    If you are including template support (by defining either `template` and/or\n    `template_stack`), and the thing the module is enabling the management of is\n    an "importable", you should define either `vsys_importable` (whose default\n    value is None) or `vsys` (whose default value is \'vsys1\').\n\n    Arguments:\n        vsys: The vsys (default: \'vsys1\').\n        device_group: Panorama only - The device group (default: \'shared\').\n        vsys_dg: The param name if vsys and device_group are a shared param.\n        vsys_importable: Either this or `vsys` should be specified.  For:\n            - Interfaces\n            - VLANs\n            - Virtual Wires\n            - Virtual Routers\n        rulebase: This is a policy of some sort.\n        template: Panorama - The template name.\n        template_stack: Panorama - The template stack name.\n        with_classic_provider_spec(bool): Include the ip_address, username,\n            password, api_key, and port params in the base spec, and make the\n            "provider" param optional.\n        with_state(bool): Include the standard \'state\' param.\n        argument_spec(dict): The argument spec to mixin with the\n            generated spec based on the given parameters.\n        required_one_of(list): List of lists to extend into required_one_of.\n        min_pandevice_version(tuple): Minimum pandevice version allowed.\n        min_panos_version(tuple): Minimum PAN-OS version allowed.\n        panorama_error(str): The error message if the device is Panorama.\n        firewall_error(str): The error message if the device is a firewall.\n\n    Returns:\n        ConnectionHelper\n    '
    helper = ConnectionHelper(min_pandevice_version, min_panos_version, panorama_error, firewall_error)
    req = []
    spec = {
        'provider': {
            'required': True,
            'type': 'dict',
            'required_one_of': [['password', 'api_key']],
            'options': {
                'host': {
                    'required': True,
                },
                'username': {
                    'default': 'admin',
                },
                'password': {
                    'no_log': True,
                },
                'api_key': {
                    'no_log': True,
                },
                'port': {
                    'default': 443,
                    'type': 'int',
                },
            },
        },
    }
    if with_classic_provider_spec:
        spec['provider']['required'] = False
        spec['provider']['options']['host']['required'] = False
        del spec['provider']['required_one_of']
        spec.update({
            'ip_address': {
                'required': False,
            },
            'username': {
                'default': 'admin',
            },
            'password': {
                'no_log': True,
            },
            'api_key': {
                'no_log': True,
            },
            'port': {
                'default': 443,
                'type': 'int',
            },
        })
        req.extend([['provider', 'ip_address'], ['provider', 'password', 'api_key']])
    if with_state:
        spec['state'] = {
            'default': 'present',
            'choices': ['present', 'absent'],
        }
    if (vsys_dg is not None):
        if isinstance(vsys_dg, bool):
            param = 'vsys_dg'
        else:
            param = vsys_dg
        spec[param] = {
            
        }
        helper.vsys_dg = param
    else:
        if (vsys is not None):
            if isinstance(vsys, bool):
                param = 'vsys'
            else:
                param = vsys
            spec[param] = {
                'default': 'vsys1',
            }
            helper.vsys = param
        if (device_group is not None):
            if isinstance(device_group, bool):
                param = 'device_group'
            else:
                param = device_group
            spec[param] = {
                'default': 'shared',
            }
            helper.device_group = param
        if (vsys_importable is not None):
            if (vsys is not None):
                raise KeyError('Define "vsys" or "vsys_importable", not both.')
            if isinstance(vsys_importable, bool):
                param = 'vsys'
            else:
                param = vsys_importable
            spec[param] = {
                
            }
            helper.vsys_importable = param
    if (rulebase is not None):
        if isinstance(rulebase, bool):
            param = 'rulebase'
        else:
            param = rulebase
        spec[param] = {
            'default': None,
            'choices': ['pre-rulebase', 'rulebase', 'post-rulebase'],
        }
        helper.rulebase = param
    if (template is not None):
        if isinstance(template, bool):
            param = 'template'
        else:
            param = template
        spec[param] = {
            
        }
        helper.template = param
    if (template_stack is not None):
        if isinstance(template_stack, bool):
            param = 'template_stack'
        else:
            param = template_stack
        spec[param] = {
            
        }
        helper.template_stack = param
    if (argument_spec is not None):
        for k in argument_spec.keys():
            if (k in spec):
                raise KeyError('{0}: key used by connection helper.'.format(k))
            spec[k] = argument_spec[k]
    if (required_one_of is not None):
        req.extend(required_one_of)
    helper.argument_spec = spec
    helper.required_one_of = req
    return helper