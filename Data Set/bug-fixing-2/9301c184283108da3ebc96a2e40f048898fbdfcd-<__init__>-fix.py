

def __init__(self, playbooks, inventory, variable_manager, loader, passwords):
    self._playbooks = playbooks
    self._inventory = inventory
    self._variable_manager = variable_manager
    self._loader = loader
    self.passwords = passwords
    self._unreachable_hosts = dict()
    if (context.CLIARGS.get('listhosts') or context.CLIARGS.get('listtasks') or context.CLIARGS.get('listtags') or context.CLIARGS.get('syntax')):
        self._tqm = None
    else:
        self._tqm = TaskQueueManager(inventory=inventory, variable_manager=variable_manager, loader=loader, passwords=self.passwords, forks=context.CLIARGS.get('forks'))
    check_for_controlpersist(C.ANSIBLE_SSH_EXECUTABLE)
