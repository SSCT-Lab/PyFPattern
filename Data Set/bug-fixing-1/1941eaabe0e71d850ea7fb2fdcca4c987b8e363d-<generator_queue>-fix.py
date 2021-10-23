

def generator_queue(generator, max_q_size=10, wait_time=0.05, nb_worker=1, pickle_safe=False):
    'Builds a queue out of a data generator.\n    If pickle_safe, use a multiprocessing approach. Else, use threading.\n    Used in `fit_generator`, `evaluate_generator`, `predict_generator`.\n\n    '
    generator_threads = []
    if pickle_safe:
        q = multiprocessing.Queue(maxsize=max_q_size)
        _stop = multiprocessing.Event()
        lock = multiprocessing.Lock()
    else:
        q = queue.Queue()
        _stop = threading.Event()
        lock = threading.Lock()
    try:

        def data_generator_task():
            while (not _stop.is_set()):
                try:
                    if (pickle_safe or (q.qsize() < max_q_size)):
                        lock.acquire()
                        generator_output = next(generator)
                        lock.release()
                        q.put(generator_output)
                    else:
                        time.sleep(wait_time)
                except Exception:
                    _stop.set()
                    raise
        for i in range(nb_worker):
            if pickle_safe:
                np.random.seed()
                thread = multiprocessing.Process(target=data_generator_task)
            else:
                thread = threading.Thread(target=data_generator_task)
            generator_threads.append(thread)
            thread.daemon = True
            thread.start()
    except:
        _stop.set()
        if pickle_safe:
            for p in generator_threads:
                if p.is_alive():
                    p.terminate()
            q.close()
        raise
    return (q, _stop)
