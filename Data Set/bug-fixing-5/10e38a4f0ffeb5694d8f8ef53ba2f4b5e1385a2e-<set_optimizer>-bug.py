def set_optimizer(self, optimizer):
    ' Registers an optimizer with the store.\n\n        When there are multiple machines, this operation (invoked from a worker node)\n        will pack the optimizer and send it to all servers. It returns after\n        this action is done.\n\n        Parameters\n        ----------\n        optimizer : Optimizer\n            the optimizer\n        '
    is_worker = ctypes.c_int()
    check_call(_LIB.MXKVStoreIsWorkerNode(ctypes.byref(is_worker)))
    if (('dist' in self.type) and is_worker.value):
        try:
            optim_str = pickle.dumps(optimizer, 0)
        except:
            raise
        self._send_command_to_servers(0, optim_str)
    else:
        self._set_updater(opt.get_updater(optimizer))