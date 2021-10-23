def network_inventory(remotes):
    '\n    :type remotes: list[AnsibleCoreCI]\n    :rtype: str\n    '
    groups = dict([(remote.platform, []) for remote in remotes])
    for remote in remotes:
        options = dict(ansible_host=remote.connection.hostname, ansible_user=remote.connection.username, ansible_ssh_private_key_file=remote.ssh_key.key, ansible_network_os=remote.platform)
        groups[remote.platform].append(('%s %s' % (remote.name.replace('.', '_'), ' '.join((('%s="%s"' % (k, options[k])) for k in sorted(options))))))
    template = ''
    for group in groups:
        hosts = '\n'.join(groups[group])
        template += (textwrap.dedent('\n        [%s]\n        %s\n        ') % (group, hosts))
    inventory = template
    return inventory