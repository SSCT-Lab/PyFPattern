def generate_batch(batch_size, num_skips, skip_window):
    global data_index
    assert ((batch_size % num_skips) == 0)
    assert (num_skips <= (2 * skip_window))
    batch = np.ndarray(shape=batch_size, dtype=np.int32)
    labels = np.ndarray(shape=(batch_size, 1), dtype=np.int32)
    span = ((2 * skip_window) + 1)
    buffer = collections.deque(maxlen=span)
    if ((data_index + span) > len(data)):
        data_index = 0
    buffer.extend(data[data_index:(data_index + span)])
    data_index += span
    for i in range((batch_size // num_skips)):
        context_words = [w for w in range(span) if (w != skip_window)]
        words_to_use = random.sample(context_words, num_skips)
        for (j, context_word) in enumerate(words_to_use):
            batch[((i * num_skips) + j)] = buffer[skip_window]
            labels[(((i * num_skips) + j), 0)] = buffer[context_word]
        if (data_index == len(data)):
            buffer[:] = data[:span]
            data_index = span
        else:
            buffer.append(data[data_index])
            data_index += 1
    data_index = (((data_index + len(data)) - span) % len(data))
    return (batch, labels)