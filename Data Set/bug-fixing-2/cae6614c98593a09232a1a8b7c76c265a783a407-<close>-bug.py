

def close(self):
    '\n        Close this executor.\n\n        You can no longer use this executor after calling this method.\n        For the distributed training, this method would free the resource on PServers related to\n        the current Trainer.\n        TODO(typhoonzero): Define "no longer use" meaning? Can user create\n        a new Executor for the same program and run?\n        TODO(panyx0718): Why ParallelExecutor doesn\'t have close?\n\n        Example:\n            >>> cpu = core.CPUPlace()\n            >>> exe = Executor(cpu)\n            >>> ...\n            >>> exe.close()\n        '
    if (not self._closed):
        self._default_executor.close()
        self._closed = True
