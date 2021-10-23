def main():
    host_list = ['localhost', 'www.example.com', 'www.google.com']
    context.CLIARGS = ImmutableDict(connection='smart', module_path=['/usr/share/ansible'], forks=10, become=None, become_method=None, become_user=None, check=False, diff=False)
    sources = ','.join(host_list)
    if (len(host_list) == 1):
        sources += ','
    loader = DataLoader()
    passwords = dict()
    inventory = InventoryManager(loader=loader, sources=sources)
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    play_source = dict(name='Ansible Play', hosts=host_list, gather_facts='no', tasks=[dict(action=dict(module='command', args=dict(cmd='/usr/bin/uptime')))])
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
    tqm = None
    callback = ResultsCollector()
    try:
        tqm = TaskQueueManager(inventory=inventory, variable_manager=variable_manager, loader=loader, passwords=passwords, stdout_callback=callback)
        result = tqm.run(play)
    finally:
        if (tqm is not None):
            tqm.cleanup()
        if loader:
            loader.cleanup_all_tmp_files()
    print('UP ***********')
    for (host, result) in callback.host_ok.items():
        print('{0} >>> {1}'.format(host, result._result['stdout']))
    print('FAILED *******')
    for (host, result) in callback.host_failed.items():
        print('{0} >>> {1}'.format(host, result._result['msg']))
    print('DOWN *********')
    for (host, result) in callback.host_unreachable.items():
        print('{0} >>> {1}'.format(host, result._result['msg']))