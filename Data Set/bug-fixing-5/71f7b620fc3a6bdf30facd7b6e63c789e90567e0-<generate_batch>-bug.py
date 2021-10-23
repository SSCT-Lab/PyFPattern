def generate_batch(batch_size, num_skips, skip_window):
    global data_index
    assert ((batch_size % num_skips) == 0)
    assert (num_skips <= (2 * skip_window))
    batch = np.ndarray(shape=batch_size, dtype=np.int32)
    labels = np.ndarray(shape=(batch_size, 1), dtype=np.int32)
    span = ((2 * skip_window) + 1)
    buffer = collections.deque(maxlen=span)
    for _ in range(span):
        buffer.append(data[data_index])
        data_index = ((data_index + 1) % len(data))
    for i in range((batch_size // num_skips)):
        target = skip_window
        targets_to_avoid = [skip_window]
        for j in range(num_skips):
            while (target in targets_to_avoid):
                target = random.randint(0, (span - 1))
            targets_to_avoid.append(target)
            batch[((i * num_skips) + j)] = buffer[skip_window]
            labels[(((i * num_skips) + j), 0)] = buffer[target]
        buffer.append(data[data_index])
        data_index = ((data_index + 1) % len(data))
    return (batch, labels)