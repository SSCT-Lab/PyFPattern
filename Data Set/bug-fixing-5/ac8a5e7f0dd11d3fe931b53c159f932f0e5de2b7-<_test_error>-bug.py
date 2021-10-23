def _test_error(self, loader):
    it = iter(loader)
    errors = 0
    while True:
        try:
            it.next()
        except NotImplementedError:
            msg = ''.join(traceback.format_exception(*sys.exc_info()))
            self.assertTrue(('collate_fn' in msg))
            errors += 1
        except StopIteration:
            self.assertEqual(errors, math.ceil((float(len(loader.dataset)) / loader.batch_size)))
            return