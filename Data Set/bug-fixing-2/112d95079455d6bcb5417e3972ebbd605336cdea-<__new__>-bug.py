

def __new__(cls, module):
    'Return the platform-specific subclass.\n\n        It does not use load_platform_subclass() because it need to judge based\n        on whether the `timedatectl` command exists.\n\n        Args:\n            module: The AnsibleModule.\n        '
    if (get_platform() == 'Linux'):
        if (module.get_bin_path('timedatectl') is not None):
            return super(Timezone, SystemdTimezone).__new__(SystemdTimezone)
        else:
            return super(Timezone, NosystemdTimezone).__new__(NosystemdTimezone)
    else:
        return super(Timezone, Timezone).__new__(Timezone)
