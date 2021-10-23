def reader_creator(pos_pattern, neg_pattern, word_idx, buffer_size):
    UNK = word_idx['<unk>']
    qs = [Queue.Queue(maxsize=buffer_size), Queue.Queue(maxsize=buffer_size)]

    def load(pattern, queue):
        for doc in tokenize(pattern):
            queue.put(doc)
        queue.put(None)

    def reader():
        t0 = threading.Thread(target=load, args=(pos_pattern, qs[0]))
        t0.daemon = True
        t0.start()
        t1 = threading.Thread(target=load, args=(neg_pattern, qs[1]))
        t1.daemon = True
        t1.start()
        i = 0
        doc = qs[i].get()
        while (doc != None):
            (yield ([word_idx.get(w, UNK) for w in doc], (i % 2)))
            i += 1
            doc = qs[(i % 2)].get()
        i += 1
        doc = qs[(i % 2)].get()
        while (doc != None):
            (yield ([word_idx.get(w, UNK) for w in doc], (i % 2)))
            doc = qs[(i % 2)].get()
    return reader()