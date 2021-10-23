@unittest.skipIf(IS_WINDOWS, 'TODO: need to fix this test case for Windows')
def test_timeout(self):

    def _test_timeout():
        os.close(sys.stderr.fileno())
        sys.stderr.close()
        dataset = SleepDataset(10, 10)
        dataloader = DataLoader(dataset, batch_size=2, num_workers=2, timeout=1)
        _ = next(iter(dataloader))
    p = multiprocessing.Process(target=_test_timeout)
    p.start()
    p.join(3.0)
    try:
        self.assertFalse(p.is_alive())
        self.assertNotEqual(p.exitcode, 0)
    finally:
        p.terminate()