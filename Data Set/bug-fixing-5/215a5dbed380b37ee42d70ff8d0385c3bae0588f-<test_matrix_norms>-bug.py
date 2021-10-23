def test_matrix_norms(self):
    np.random.seed(1234)
    for (n, m) in ((1, 1), (1, 3), (3, 1), (4, 4), (4, 5), (5, 4)):
        for t in (np.single, np.double, np.csingle, np.cdouble, np.int64):
            A = (10 * np.random.randn(n, m).astype(t))
            if np.issubdtype(A.dtype, np.complexfloating):
                A = (A + (10j * np.random.randn(n, m))).astype(t)
                t_high = np.cdouble
            else:
                t_high = np.double
            for order in (None, 'fro', 1, (- 1), 2, (- 2), np.inf, (- np.inf)):
                actual = norm(A, ord=order)
                desired = np.linalg.norm(A, ord=order)
                if (not np.allclose(actual, desired)):
                    desired = np.linalg.norm(A.astype(t_high), ord=order)
                    np.assert_allclose(actual, desired)