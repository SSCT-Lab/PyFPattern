def check(self, data=None, dtype=None, dtypes=None):
    'Check the special function against the data.'
    if self.knownfailure:
        pytest.xfail(reason=self.knownfailure)
    if (data is None):
        data = self.data
    if (dtype is None):
        dtype = data.dtype
    else:
        data = data.astype(dtype)
    (rtol, atol) = self.get_tolerances(dtype)
    if self.param_filter:
        param_mask = np.ones((data.shape[0],), np.bool_)
        for (j, filter) in zip(self.param_columns, self.param_filter):
            if filter:
                param_mask &= list(filter(data[:, j]))
        data = data[param_mask]
    params = []
    for (idx, j) in enumerate(self.param_columns):
        if np.iscomplexobj(j):
            j = int(j.imag)
            params.append(data[:, j].astype(complex))
        elif (dtypes and (idx < len(dtypes))):
            params.append(data[:, j].astype(dtypes[idx]))
        else:
            params.append(data[:, j])

    def eval_func_at_params(func, skip_mask=None):
        if self.vectorized:
            got = func(*params)
        else:
            got = []
            for j in range(len(params[0])):
                if ((skip_mask is not None) and skip_mask[j]):
                    got.append(np.nan)
                    continue
                got.append(func(*tuple([params[i][j] for i in range(len(params))])))
            got = np.asarray(got)
        if (not isinstance(got, tuple)):
            got = (got,)
        return got
    got = eval_func_at_params(self.func)
    if (self.result_columns is not None):
        wanted = tuple([data[:, icol] for icol in self.result_columns])
    else:
        skip_mask = None
        if (self.nan_ok and (len(got) == 1)):
            skip_mask = np.isnan(got[0])
        wanted = eval_func_at_params(self.result_func, skip_mask=skip_mask)
    assert_((len(got) == len(wanted)))
    for (output_num, (x, y)) in enumerate(zip(got, wanted)):
        if (np.issubdtype(x.dtype, np.complexfloating) or self.ignore_inf_sign):
            pinf_x = np.isinf(x)
            pinf_y = np.isinf(y)
            minf_x = np.isinf(x)
            minf_y = np.isinf(y)
        else:
            pinf_x = np.isposinf(x)
            pinf_y = np.isposinf(y)
            minf_x = np.isneginf(x)
            minf_y = np.isneginf(y)
        nan_x = np.isnan(x)
        nan_y = np.isnan(y)
        olderr = np.seterr(all='ignore')
        try:
            abs_y = np.absolute(y)
            abs_y[(~ np.isfinite(abs_y))] = 0
            diff = np.absolute((x - y))
            diff[(~ np.isfinite(diff))] = 0
            rdiff = (diff / np.absolute(y))
            rdiff[(~ np.isfinite(rdiff))] = 0
        finally:
            np.seterr(**olderr)
        tol_mask = (diff <= (atol + (rtol * abs_y)))
        pinf_mask = (pinf_x == pinf_y)
        minf_mask = (minf_x == minf_y)
        nan_mask = (nan_x == nan_y)
        bad_j = (~ (((tol_mask & pinf_mask) & minf_mask) & nan_mask))
        point_count = bad_j.size
        if self.nan_ok:
            bad_j &= (~ nan_x)
            bad_j &= (~ nan_y)
            point_count -= (nan_x | nan_y).sum()
        if ((not self.distinguish_nan_and_inf) and (not self.nan_ok)):
            inf_x = np.isinf(x)
            inf_y = np.isinf(y)
            both_nonfinite = ((inf_x & nan_y) | (nan_x & inf_y))
            bad_j &= (~ both_nonfinite)
            point_count -= both_nonfinite.sum()
        if np.any(bad_j):
            msg = ['']
            msg.append(('Max |adiff|: %g' % diff[bad_j].max()))
            msg.append(('Max |rdiff|: %g' % rdiff[bad_j].max()))
            msg.append(('Bad results (%d out of %d) for the following points (in output %d):' % (np.sum(bad_j), point_count, output_num)))
            for j in np.nonzero(bad_j)[0]:
                j = int(j)
                fmt = (lambda x: ('%30s' % np.array2string(x[j], precision=18)))
                a = '  '.join(map(fmt, params))
                b = '  '.join(map(fmt, got))
                c = '  '.join(map(fmt, wanted))
                d = fmt(rdiff)
                msg.append(('%s => %s != %s  (rdiff %s)' % (a, b, c, d)))
            assert_(False, '\n'.join(msg))