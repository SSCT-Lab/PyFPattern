

def random_worker_loop(datasets, key_queue, data_queue, batchify_fn):
    'Worker loop for multiprocessing DataLoader with multiple transform functions.'
    limit = sys.getrecursionlimit()
    max_recursion_depth = min((limit - 5), max(10, (limit // 2)))
    _recursive_fork_recordio(dataset, 0, max_recursion_depth)
    while True:
        (idx, samples, random_idx) = key_queue.get()
        if (idx is None):
            break
        batch = batchify_fn([datasets[random_idx][i] for i in samples])
        data_queue.put((idx, batch))
