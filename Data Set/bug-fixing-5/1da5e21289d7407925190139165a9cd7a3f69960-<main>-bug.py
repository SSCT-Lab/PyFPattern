def main():
    host_list = ['localhost', 'www.example.com', 'www.google.com']
    Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check', 'diff'])
    sources = ','.join(host_list)
    if (len(host_list) == 1):
        sources += ','
    loader = DataLoader()
    options = Options(connection='smart', module_path=['/usr/share/ansible'], forks=100, remote_user=None, private_key_file=None, ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None, become_user=None, verbosity=None, check=False, diff=False)
    passwords = dict()
    inventory = InventoryManager(loader=loader, sources=sources)
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    play_source = dict(name='Ansible Play', hosts=host_list, gather_facts='no', tasks=[dict(action=dict(module='command', args=dict(cmd='/usr/bin/uptime')))])
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
    tqm = None
    callback = ResultsCollector()
    try:
        tqm = TaskQueueManager(inventory=inventory, variable_manager=variable_manager, loader=loader, options=options, passwords=passwords)
        tqm._stdout_callback = callback
        result = tqm.run(play)
    finally:
        if (tqm is not None):
            tqm.cleanup()
    print('UP ***********')
    for (host, result) in callback.host_ok.items():
        print('{0} >>> {1}'.format(host, result._result['stdout']))
    print('FAILED *******')
    for (host, result) in callback.host_failed.items():
        print('{0} >>> {1}'.format(host, result._result['msg']))
    print('DOWN *********')
    for (host, result) in callback.host_unreachable.items():
        print('{0} >>> {1}'.format(host, result._result['msg']))