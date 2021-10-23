

def summary_col(results, float_format='%.4f', model_names=(), stars=False, info_dict=None, regressor_order=(), drop_omitted=False):
    '\n    Summarize multiple results instances side-by-side (coefs and SEs)\n\n    Parameters\n    ----------\n    results : statsmodels results instance or list of result instances\n    float_format : str, optional\n        float format for coefficients and standard errors\n        Default : \'%.4f\'\n    model_names : list[str], optional\n        Must have same length as the number of results. If the names are not\n        unique, a roman number will be appended to all model names\n    stars : bool\n        print significance stars\n    info_dict : dict\n        dict of functions to be applied to results instances to retrieve\n        model info. To use specific information for different models, add a\n        (nested) info_dict with model name as the key.\n        Example: `info_dict = {"N":..., "R2": ..., "OLS":{"R2":...}}` would\n        only show `R2` for OLS regression models, but additionally `N` for\n        all other results.\n        Default : None (use the info_dict specified in\n        result.default_model_infos, if this property exists)\n    regressor_order : list[str], optional\n        list of names of the regressors in the desired order. All regressors\n        not specified will be appended to the end of the list.\n    drop_omitted : bool, optional\n        Includes regressors that are not specified in regressor_order. If\n        False, regressors not specified will be appended to end of the list.\n        If True, only regressors in regressor_order will be included.\n    '
    if (not isinstance(results, list)):
        results = [results]
    cols = [_col_params(x, stars=stars, float_format=float_format) for x in results]
    if model_names:
        colnames = _make_unique(model_names)
    else:
        colnames = _make_unique([x.columns[0] for x in cols])
    for i in range(len(cols)):
        cols[i].columns = [colnames[i]]

    def merg(x, y):
        return x.merge(y, how='outer', right_index=True, left_index=True)
    summ = reduce(merg, cols)
    if regressor_order:
        varnames = summ.index.get_level_values(0).tolist()
        ordered = [x for x in regressor_order if (x in varnames)]
        unordered = [x for x in varnames if (x not in (regressor_order + ['']))]
        order = (ordered + list(np.unique(unordered)))

        def f(idx):
            return sum([[(x + 'coef'), (x + 'stde')] for x in idx], [])
        summ.index = f(pd.unique(varnames))
        summ = summ.reindex(f(order))
        summ.index = [x[:(- 4)] for x in summ.index]
        if drop_omitted:
            summ = summ.loc[regressor_order]
    idx = ((pd.Series(lrange(summ.shape[0])) % 2) == 1)
    summ.index = np.where(idx, '', summ.index.get_level_values(0))
    if info_dict:
        cols = [_col_info(x, info_dict.get(x.model.__class__.__name__, info_dict)) for x in results]
    else:
        cols = [_col_info(x, getattr(x, 'default_model_infos', None)) for x in results]
    for (df, name) in zip(cols, _make_unique([df.columns[0] for df in cols])):
        df.columns = [name]

    def merg(x, y):
        return x.merge(y, how='outer', right_index=True, left_index=True)
    info = reduce(merg, cols)
    dat = pd.DataFrame(np.vstack([summ, info]))
    dat.columns = summ.columns
    dat.index = pd.Index((summ.index.tolist() + info.index.tolist()))
    summ = dat
    summ = summ.fillna('')
    smry = Summary()
    smry._merge_latex = True
    smry.add_df(summ, header=True, align='l')
    smry.add_text('Standard errors in parentheses.')
    if stars:
        smry.add_text('* p<.1, ** p<.05, ***p<.01')
    return smry
