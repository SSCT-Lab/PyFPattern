def random_worker_loop(datasets, key_queue, data_queue, batchify_fn):
    'Worker loop for multiprocessing DataLoader with multiple transform functions.'
    for dataset in datasets:
        dataset._fork()
    while True:
        (idx, samples, random_idx) = key_queue.get()
        if (idx is None):
            break
        batch = batchify_fn([datasets[random_idx][i] for i in samples])
        data_queue.put((idx, batch))