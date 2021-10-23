

def get_cmd(m, subcommand):
    'puts together the basic zypper command arguments with those passed to the module'
    is_install = (subcommand in ['install', 'update', 'patch', 'dist-upgrade'])
    is_refresh = (subcommand == 'refresh')
    cmd = ['/usr/bin/zypper', '--quiet', '--non-interactive', '--xmlout']
    if ((is_install or is_refresh) and m.params['disable_gpg_check']):
        cmd.append('--no-gpg-checks')
    if (subcommand == 'search'):
        cmd.append('--disable-repositories')
    cmd.append(subcommand)
    if ((subcommand not in ['patch', 'dist-upgrade']) and (not is_refresh)):
        cmd.extend(['--type', m.params['type']])
    if (m.check_mode and (subcommand != 'search')):
        cmd.append('--dry-run')
    if is_install:
        cmd.append('--auto-agree-with-licenses')
        if m.params['disable_recommends']:
            cmd.append('--no-recommends')
        if m.params['force']:
            cmd.append('--force')
        if m.params['oldpackage']:
            cmd.append('--oldpackage')
    if m.params['extra_args']:
        args_list = m.params['extra_args'].split(' ')
        cmd.extend(args_list)
    return cmd
