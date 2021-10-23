def __init__(self, inventory, variable_manager, loader, options, passwords, stdout_callback=None, run_additional_callbacks=True, run_tree=False):
    self._inventory = inventory
    self._variable_manager = variable_manager
    self._loader = loader
    self._options = options
    self._stats = AggregateStats()
    self.passwords = passwords
    self._stdout_callback = stdout_callback
    self._run_additional_callbacks = run_additional_callbacks
    self._run_tree = run_tree
    self._callbacks_loaded = False
    self._callback_plugins = []
    self._start_at_done = False
    if options.module_path:
        for path in options.module_path:
            if path:
                module_loader.add_directory(path)
    self._terminated = False
    self._notified_handlers = dict()
    self._listening_handlers = dict()
    self._failed_hosts = dict()
    self._unreachable_hosts = dict()
    self._final_q = multiprocessing.Queue()
    self._connection_lockfile = tempfile.TemporaryFile()