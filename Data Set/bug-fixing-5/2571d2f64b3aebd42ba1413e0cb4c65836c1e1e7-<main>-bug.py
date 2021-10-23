def main():
    ' Entry point for ansible module. '
    module = AnsibleModule(argument_spec={
        'table': {
            'required': True,
        },
        'record': {
            'required': True,
        },
        'col': {
            'required': True,
        },
        'key': {
            'required': True,
        },
        'value': {
            'required': True,
        },
        'timeout': {
            'default': 5,
            'type': 'int',
        },
    }, supports_check_mode=True)
    params_set(module)