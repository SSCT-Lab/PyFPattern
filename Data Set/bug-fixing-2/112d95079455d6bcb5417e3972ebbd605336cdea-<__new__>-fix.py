

def __new__(cls, module):
    'Return the platform-specific subclass.\n\n        It does not use load_platform_subclass() because it need to judge based\n        on whether the `timedatectl` command exists and available.\n\n        Args:\n            module: The AnsibleModule.\n        '
    if (get_platform() == 'Linux'):
        timedatectl = module.get_bin_path('timedatectl')
        if ((timedatectl is not None) and (module.run_command(timedatectl)[0] == 0)):
            return super(Timezone, SystemdTimezone).__new__(SystemdTimezone)
        else:
            return super(Timezone, NosystemdTimezone).__new__(NosystemdTimezone)
    else:
        return super(Timezone, Timezone).__new__(Timezone)
