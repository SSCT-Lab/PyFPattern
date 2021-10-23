def get_connection(vsys=None, device_group=None, vsys_dg=None, vsys_importable=None, rulebase=None, template=None, template_stack=None, classic_provider_spec=False, panorama_error=None, firewall_error=None):
    'Returns a helper object that handles pandevice object tree init.\n\n    All arguments to this function (except panorama_error, firewall_error,\n    and classic_provider_spec) can be any of the following types:\n\n        * None - do not include this in the spec\n        * True - use the default param name\n        * string - use this string for the param name\n\n    Arguments:\n        vsys: Firewall only - The vsys.\n        device_group: Panorama only - The device group.\n        vsys_dg: The param name if vsys and device_group are a shared param.\n        vsys_importable: Either this or `vsys` should be specified.  For:\n            - Interfaces\n            - VLANs\n            - Virtual Wires\n            - Virtual Routers\n        rulebase: This is a policy of some sort.\n        template: Panorama - The template name.\n        template_stack: Panorama - The template stack name.\n        classic_provider_spec(bool): Include the ip_address, username,\n            password, api_key params in the base spec, and make the\n            "provider" param optional.\n        panorama_error(str): The error message if the device is Panorama.\n        firewall_error(str): The error message if the device is a firewall.\n\n    Returns:\n        ConnectionHelper\n    '
    helper = ConnectionHelper(panorama_error, firewall_error)
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
            },
        },
    }
    if classic_provider_spec:
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
        })
        req.extend([['provider', 'ip_address'], ['provider', 'password', 'api_key']])
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
            'default': 'pre-rulebase',
            'choices': ['pre-rulebase', 'post-rulebase'],
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
    helper.argument_spec = spec
    helper.required_one_of = req
    return helper