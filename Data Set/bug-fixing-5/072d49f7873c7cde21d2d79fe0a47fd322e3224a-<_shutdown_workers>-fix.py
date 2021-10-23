def _shutdown_workers(self):
    try:
        if (not self.shutdown):
            self.shutdown = True
            self.done_event.set()
            for q in self.index_queues:
                q.put(None)
            try:
                while (not self.worker_result_queue.empty()):
                    self.worker_result_queue.get()
            except (FileNotFoundError, ImportError):
                pass
            self.worker_result_queue.put(None)
    finally:
        if self.worker_pids_set:
            _remove_worker_pids(id(self))
            self.worker_pids_set = False