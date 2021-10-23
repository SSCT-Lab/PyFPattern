@ignore_warnings
def test_multilabel_representation_invariance():
    n_classes = 4
    n_samples = 50
    (_, y1) = make_multilabel_classification(n_features=1, n_classes=n_classes, random_state=0, n_samples=n_samples, allow_unlabeled=True)
    (_, y2) = make_multilabel_classification(n_features=1, n_classes=n_classes, random_state=1, n_samples=n_samples, allow_unlabeled=True)
    y1 += ([0] * n_classes)
    y2 += ([0] * n_classes)
    y1_sparse_indicator = sp.coo_matrix(y1)
    y2_sparse_indicator = sp.coo_matrix(y2)
    for name in MULTILABELS_METRICS:
        metric = ALL_METRICS[name]
        if isinstance(metric, partial):
            metric.__module__ = 'tmp'
            metric.__name__ = name
        measure = metric(y1, y2)
        assert_almost_equal(metric(y1_sparse_indicator, y2_sparse_indicator), measure, err_msg=('%s failed representation invariance  between dense and sparse indicator formats.' % name))