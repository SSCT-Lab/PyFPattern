

def test_vcomp_2(self):
    np.random.seed(6241)
    n = 1600
    exog = np.random.normal(size=(n, 2))
    groups = np.kron(np.arange((n / 16)), np.ones(16))
    errors = 0
    exog_re = np.random.normal(size=(n, 2))
    slopes = np.random.normal(size=((n / 16), 2))
    slopes = (np.kron(slopes, np.ones((16, 1))) * exog_re)
    errors += slopes.sum(1)
    subgroups1 = np.kron(np.arange((n / 4)), np.ones(4))
    errors += np.kron((2 * np.random.normal(size=(n // 4))), np.ones(4))
    subgroups2 = np.kron(np.arange((n / 2)), np.ones(2))
    errors += np.kron((2 * np.random.normal(size=(n // 2))), np.ones(2))
    errors += np.random.normal(size=n)
    endog = (exog.sum(1) + errors)
    df = pd.DataFrame(index=range(n))
    df['y'] = endog
    df['groups'] = groups
    df['x1'] = exog[:, 0]
    df['x2'] = exog[:, 1]
    df['z1'] = exog_re[:, 0]
    df['z2'] = exog_re[:, 1]
    df['v1'] = subgroups1
    df['v2'] = subgroups2
    vcf = {
        'a': '0 + C(v1)',
        'b': '0 + C(v2)',
    }
    model1 = MixedLM.from_formula('y ~ x1 + x2', groups=groups, re_formula='0+z1+z2', vc_formula=vcf, data=df)
    result1 = model1.fit()
    assert_allclose(result1.fe_params, [0.16527, 0.99911, 0.96217], rtol=0.0001)
    assert_allclose(result1.cov_re, [[1.244, 0.146], [0.146, 1.371]], rtol=0.001)
    assert_allclose(result1.vcomp, [4.024, 3.997], rtol=0.001)
    assert_allclose(result1.bse.iloc[0:3], [0.1261, 0.03938, 0.03848], rtol=0.001)
