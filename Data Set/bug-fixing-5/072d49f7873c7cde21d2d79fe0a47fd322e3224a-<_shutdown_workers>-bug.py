def _shutdown_workers(self):
    try:
        if (not self.shutdown):
            self.shutdown = True
            self.done_event.set()
            try:
                while (not self.data_queue.empty()):
                    self.data_queue.get()
            except FileNotFoundError:
                pass
            for q in self.index_queues:
                q.put(None)
            self.worker_result_queue.put(None)
    finally:
        if self.worker_pids_set:
            _remove_worker_pids(id(self))
            self.worker_pids_set = False