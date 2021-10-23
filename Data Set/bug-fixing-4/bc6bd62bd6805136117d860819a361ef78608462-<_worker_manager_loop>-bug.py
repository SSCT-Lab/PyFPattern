def _worker_manager_loop(in_queue, out_queue, done_event, pin_memory):
    while True:
        try:
            r = in_queue.get()
        except Exception:
            if done_event.is_set():
                return
            raise
        if (r is None):
            break
        if isinstance(r[1], ExceptionWrapper):
            out_queue.put(r)
            continue
        (idx, batch) = r
        try:
            if pin_memory:
                batch = pin_memory_batch(batch)
        except Exception:
            out_queue.put((idx, ExceptionWrapper(sys.exc_info())))
        else:
            out_queue.put((idx, batch))