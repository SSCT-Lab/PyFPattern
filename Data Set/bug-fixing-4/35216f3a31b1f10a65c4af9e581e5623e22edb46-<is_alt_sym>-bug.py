def is_alt_sym(self, eps=0.05, _random_prec=None):
    'Monte Carlo test for the symmetric/alternating group for degrees\n        >= 8.\n\n        More specifically, it is one-sided Monte Carlo with the\n        answer True (i.e., G is symmetric/alternating) guaranteed to be\n        correct, and the answer False being incorrect with probability eps.\n\n        For degree < 8, the order of the group is checked so the test\n        is deterministic.\n\n        Notes\n        =====\n\n        The algorithm itself uses some nontrivial results from group theory and\n        number theory:\n        1) If a transitive group ``G`` of degree ``n`` contains an element\n        with a cycle of length ``n/2 < p < n-2`` for ``p`` a prime, ``G`` is the\n        symmetric or alternating group ([1], pp. 81-82)\n        2) The proportion of elements in the symmetric/alternating group having\n        the property described in 1) is approximately `\\log(2)/\\log(n)`\n        ([1], p.82; [2], pp. 226-227).\n        The helper function ``_check_cycles_alt_sym`` is used to\n        go over the cycles in a permutation and look for ones satisfying 1).\n\n        Examples\n        ========\n\n        >>> from sympy.combinatorics.perm_groups import PermutationGroup\n        >>> from sympy.combinatorics.named_groups import DihedralGroup\n        >>> D = DihedralGroup(10)\n        >>> D.is_alt_sym()\n        False\n\n        See Also\n        ========\n\n        _check_cycles_alt_sym\n\n        '
    if (_random_prec is None):
        n = self.degree
        if (n < 8):
            sym_order = 1
            for i in range(2, (n + 1)):
                sym_order *= i
            order = self.order()
            return ((order == sym_order) or ((2 * order) == sym_order))
        if (not self.is_transitive()):
            return False
        if (n < 17):
            c_n = 0.34
        else:
            c_n = 0.57
        d_n = ((c_n * log(2)) / log(n))
        N_eps = int(((- log(eps)) / d_n))
        for i in range(N_eps):
            perm = self.random_pr()
            if _check_cycles_alt_sym(perm):
                return True
        return False
    else:
        for i in range(_random_prec['N_eps']):
            perm = _random_prec[i]
            if _check_cycles_alt_sym(perm):
                return True
        return False