def test_entropy_shape(self):
    for (Dist, params) in EXAMPLES:
        for (i, param) in enumerate(params):
            dist = Dist(**param)
            try:
                actual_shape = dist.entropy().size()
                expected_shape = dist._batch_shape
                if (not expected_shape):
                    expected_shape = torch.Size((1,))
                message = '{} example {}/{}, shape mismatch. expected {}, actual {}'.format(Dist.__name__, i, len(params), expected_shape, actual_shape)
                self.assertEqual(actual_shape, expected_shape, message=message)
            except NotImplementedError:
                continue