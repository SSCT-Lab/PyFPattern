@unittest.skipIf(IS_WINDOWS, 'TODO: need to fix this test case for Windows')
def test_segfault(self):

    def _test_segfault():
        sys.stderr.close()
        dataset = SegfaultDataset(10)
        dataloader = DataLoader(dataset, batch_size=2, num_workers=2)
        _ = next(iter(dataloader))
    p = multiprocessing.Process(target=_test_segfault)
    p.start()
    p.join(1.0)
    try:
        self.assertFalse(p.is_alive())
        self.assertNotEqual(p.exitcode, 0)
    finally:
        p.terminate()