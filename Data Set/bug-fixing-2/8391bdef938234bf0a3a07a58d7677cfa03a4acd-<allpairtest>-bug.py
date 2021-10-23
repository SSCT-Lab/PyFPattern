

def allpairtest(self, testfunc, alpha=0.05, method='bonf', pvalidx=1):
    "run a pairwise test on all pairs with multiple test correction\n\n        The statistical test given in testfunc is calculated for all pairs\n        and the p-values are adjusted by methods in multipletests. The p-value\n        correction is generic and based only on the p-values, and does not\n        take any special structure of the hypotheses into account.\n\n        Parameters\n        ----------\n        testfunc : function\n            A test function for two (independent) samples. It is assumed that\n            the return value on position pvalidx is the p-value.\n        alpha : float\n            familywise error rate\n        method : string\n            This specifies the method for the p-value correction. Any method\n            of multipletests is possible.\n        pvalidx : int (default: 1)\n            position of the p-value in the return of testfunc\n\n        Returns\n        -------\n        sumtab : SimpleTable instance\n            summary table for printing\n\n        errors:  TODO: check if this is still wrong, I think it's fixed.\n        results from multipletests are in different order\n        pval_corrected can be larger than 1 ???\n        "
    res = []
    for (i, j) in zip(*self.pairindices):
        res.append(testfunc(self.datali[i], self.datali[j]))
    res = np.array(res)
    (reject, pvals_corrected, alphacSidak, alphacBonf) = multipletests(res[:, pvalidx], alpha=0.05, method=method)
    (i1, i2) = self.pairindices
    if (pvals_corrected is None):
        resarr = np.array(lzip(self.groupsunique[i1], self.groupsunique[i2], np.round(res[:, 0], 4), np.round(res[:, 1], 4), reject), dtype=[('group1', object), ('group2', object), ('stat', float), ('pval', float), ('reject', np.bool8)])
    else:
        resarr = np.array(lzip(self.groupsunique[i1], self.groupsunique[i2], np.round(res[:, 0], 4), np.round(res[:, 1], 4), np.round(pvals_corrected, 4), reject), dtype=[('group1', object), ('group2', object), ('stat', float), ('pval', float), ('pval_corr', float), ('reject', np.bool8)])
    results_table = SimpleTable(resarr, headers=resarr.dtype.names)
    results_table.title = (('Test Multiple Comparison %s \n%s%4.2f method=%s' % (testfunc.__name__, 'FWER=', alpha, method)) + ('\nalphacSidak=%4.2f, alphacBonf=%5.3f' % (alphacSidak, alphacBonf)))
    return (results_table, (res, reject, pvals_corrected, alphacSidak, alphacBonf), resarr)
