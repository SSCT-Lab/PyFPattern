def grafana_plugin(module, params):
    '\n    Install update or remove grafana plugin\n\n    :param module: ansible module object. used to run system commands.\n    :param params: ansible module params.\n    '
    grafana_cli = grafana_cli_bin(params)
    if (params['state'] == 'present'):
        grafana_plugin_version = get_grafana_plugin_version(module, params)
        if (grafana_plugin_version is not None):
            if (('version' in params) and params['version']):
                if (params['version'] == grafana_plugin_version):
                    return {
                        'msg': 'Grafana plugin already installed',
                        'changed': False,
                        'version': grafana_plugin_version,
                    }
                elif ((params['version'] == 'latest') or (params['version'] is None)):
                    cmd = '{} update {}'.format(grafana_cli, params['name'])
                else:
                    cmd = '{} install {} {}'.format(grafana_cli, params['name'], params['version'])
            else:
                return {
                    'msg': 'Grafana plugin already installed',
                    'changed': False,
                    'version': grafana_plugin_version,
                }
        elif ('version' in params):
            if ((params['version'] == 'latest') or (params['version'] is None)):
                cmd = '{} install {}'.format(grafana_cli, params['name'])
            else:
                cmd = '{} install {} {}'.format(grafana_cli, params['name'], params['version'])
        else:
            cmd = '{} install {}'.format(grafana_cli, params['name'])
    else:
        cmd = '{} uninstall {}'.format(grafana_cli, params['name'])
    (rc, stdout, stderr) = module.run_command(cmd)
    if (rc == 0):
        stdout_lines = stdout.split('\n')
        for line in stdout_lines:
            if line.find(params['name']):
                (plugin_name, plugin_version) = line.split(' @ ')
                return {
                    'msg': 'Grafana plugin {} installed : {}'.format(params['name'], cmd),
                    'changed': True,
                    'version': plugin_version,
                }
    else:
        raise GrafanaCliException("'{}' execution returned an error : [{}] {} {}".format(cmd, rc, stdout, stderr))