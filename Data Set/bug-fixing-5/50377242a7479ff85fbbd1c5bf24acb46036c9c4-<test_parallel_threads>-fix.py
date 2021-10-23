def test_parallel_threads():
    lock = ReentrancyLock('failure')
    failflag = [False]
    exceptions_raised = []

    def worker(k):
        try:
            with lock:
                assert_((not failflag[0]))
                failflag[0] = True
                time.sleep((0.1 * k))
                assert_(failflag[0])
                failflag[0] = False
        except:
            exceptions_raised.append(traceback.format_exc(2))
    threads = [threading.Thread(target=(lambda k=k: worker(k))) for k in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    exceptions_raised = '\n'.join(exceptions_raised)
    assert_((not exceptions_raised), exceptions_raised)