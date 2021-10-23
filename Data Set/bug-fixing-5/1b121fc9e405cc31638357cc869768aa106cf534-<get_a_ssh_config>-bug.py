def get_a_ssh_config(box_name):
    "Gives back a map of all the machine's ssh configurations"
    output = subprocess.check_output(['vagrant', 'ssh-config', box_name])
    config = SSHConfig()
    config.parse(StringIO(output))
    host_config = config.lookup(box_name)
    for id in host_config['identityfile']:
        if os.path.isfile(id):
            host_config['identityfile'] = id
    return dict(((v, host_config[k]) for (k, v) in _ssh_to_ansible))