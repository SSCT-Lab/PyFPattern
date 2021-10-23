

def test_Xdist_deprecated_args():
    X1 = np.asarray([[1.0, 2.0, 3.0], [1.2, 2.3, 3.4], [2.2, 2.3, 4.4]])
    warn_msg = 'Got unexpected kwarg'
    for metric in _METRICS_NAMES:
        if (metric in ('minkowski', 'wminkowski', 'seuclidean', 'mahalanobis')):
            continue
        for arg in ['p', 'V', 'VI', 'w']:
            kwargs = {
                arg: 'foo',
            }
            if (metric == 'wminkowski'):
                if (('p' in kwargs) or ('w' in kwargs)):
                    continue
                kwargs['w'] = (1.0 / X1.std(axis=0))
            if (((arg == 'V') and (metric == 'seuclidean')) or ((arg == 'VI') and (metric == 'mahalanobis')) or ((arg == 'w') and (metric == 'wminkowski'))):
                continue
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter('always')
                cdist(X1, X1, metric, **kwargs)
                pdist(X1, metric, **kwargs)
                assert_((len(w) == 2))
                assert_(issubclass(w[0].category, DeprecationWarning))
                assert_(issubclass(w[1].category, DeprecationWarning))
                assert_(all([(warn_msg in str(warn.message)) for warn in w]))
