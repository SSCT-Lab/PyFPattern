def test_cdist_dtype_equivalence(self):
    eps = 1e-07
    tests = [(eo['random-bool-data'], self.valid_upcasts['bool']), (eo['random-uint-data'], self.valid_upcasts['uint']), (eo['random-int-data'], self.valid_upcasts['int']), (eo['random-float32-data'], self.valid_upcasts['float32'])]
    for metric in _metrics:
        for test in tests:
            X1 = test[0]
            try:
                y1 = pdist(X1, metric=metric)
            except Exception as e:
                e_cls = e.__class__
                if (verbose > 2):
                    print(e_cls.__name__)
                    print(e)
                for new_type in test[1]:
                    X2 = new_type(test[0])
                    assert_raises(e_cls, pdist, X2, metric=metric)
            else:
                for new_type in test[1]:
                    y2 = pdist(new_type(X1), metric=metric)
                    _assert_within_tol(y1, y2, eps, (verbose > 2))