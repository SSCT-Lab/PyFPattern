def windows_inventory(remotes):
    '\n    :type remotes: list[AnsibleCoreCI]\n    :rtype: str\n    '
    hosts = []
    for remote in remotes:
        options = dict(ansible_host=remote.connection.hostname, ansible_user=remote.connection.username, ansible_password=remote.connection.password, ansible_port=remote.connection.port)
        if remote.ssh_key:
            options['ansible_ssh_private_key_file'] = os.path.abspath(remote.ssh_key.key)
        hosts.append(('%s %s' % (remote.name.replace('/', '_'), ' '.join((('%s="%s"' % (k, options[k])) for k in sorted(options))))))
    template = '\n    [windows]\n    %s\n\n    [windows:vars]\n    ansible_connection=winrm\n    ansible_winrm_server_cert_validation=ignore\n\n    # support winrm connection tests (temporary solution, does not support testing enable/disable of pipelining)\n    [winrm:children]\n    windows\n\n    # support winrm binary module tests (temporary solution)\n    [testhost:children]\n    windows\n    '
    template = textwrap.dedent(template)
    inventory = (template % '\n'.join(hosts))
    return inventory