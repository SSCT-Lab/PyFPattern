def __new__(cls, module):
    'Return the platform-specific subclass.\n\n        It does not use load_platform_subclass() because it needs to judge based\n        on whether the `timedatectl` command exists and is available.\n\n        Args:\n            module: The AnsibleModule.\n        '
    if (get_platform() == 'Linux'):
        timedatectl = module.get_bin_path('timedatectl')
        if (timedatectl is not None):
            (rc, stdout, stderr) = module.run_command(timedatectl)
            if (rc == 0):
                return super(Timezone, SystemdTimezone).__new__(SystemdTimezone)
            else:
                module.warn(('timedatectl command was found but not usable: %s. using other method.' % stderr))
                return super(Timezone, NosystemdTimezone).__new__(NosystemdTimezone)
        else:
            return super(Timezone, NosystemdTimezone).__new__(NosystemdTimezone)
    elif re.match('^joyent_.*Z', platform.version()):
        zonename_cmd = module.get_bin_path('zonename')
        if (zonename_cmd is not None):
            (rc, stdout, _) = module.run_command(zonename_cmd)
            if ((rc == 0) and (stdout.strip() == 'global')):
                module.fail_json(msg='Adjusting timezone is not supported in Global Zone')
        return super(Timezone, SmartOSTimezone).__new__(SmartOSTimezone)
    elif re.match('^(Free|Net|Open)BSD', platform.platform()):
        return super(Timezone, BSDTimezone).__new__(BSDTimezone)
    else:
        return super(Timezone, Timezone).__new__(Timezone)