def test_parallel_threads():
    results = []
    lock = ReentrancyLock('failure')

    def worker(k):
        with lock:
            time.sleep((0.01 * (3 - k)))
            results.append(k)
    threads = [threading.Thread(target=(lambda k=k: worker(k))) for k in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert_equal(results, sorted(results))