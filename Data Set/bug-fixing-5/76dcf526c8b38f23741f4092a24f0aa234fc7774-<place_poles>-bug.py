def place_poles(A, B, poles, method='YT', rtol=0.001, maxiter=30):
    '\n    Compute K such that eigenvalues (A - dot(B, K))=poles.\n\n    K is the gain matrix such as the plant described by the linear system\n    ``AX+BU`` will have its closed-loop poles, i.e the eigenvalues ``A - B*K``,\n    as close as possible to those asked for in poles.\n\n    SISO, MISO and MIMO systems are supported.\n\n    Parameters\n    ----------\n    A, B : ndarray\n        State-space representation of linear system ``AX + BU``.\n    poles : array_like\n        Desired real poles and/or complex conjugates poles.\n        Complex poles are only supported with ``method="YT"`` (default).\n    method: {\'YT\', \'KNV0\'}, optional\n        Which method to choose to find the gain matrix K. One of:\n\n            - \'YT\': Yang Tits\n            - \'KNV0\': Kautsky, Nichols, Van Dooren update method 0\n\n        See References and Notes for details on the algorithms.\n    rtol: float, optional\n        After each iteration the determinant of the eigenvectors of\n        ``A - B*K`` is compared to its previous value, when the relative\n        error between these two values becomes lower than `rtol` the algorithm\n        stops.  Default is 1e-3.\n    maxiter: int, optional\n        Maximum number of iterations to compute the gain matrix.\n        Default is 30.\n\n    Returns\n    -------\n    full_state_feedback : Bunch object\n        full_state_feedback is composed of:\n            gain_matrix : 1-D ndarray\n                The closed loop matrix K such as the eigenvalues of ``A-BK``\n                are as close as possible to the requested poles.\n            computed_poles : 1-D ndarray\n                The poles corresponding to ``A-BK`` sorted as first the real\n                poles in increasing order, then the complex congugates in\n                lexicographic order.\n            requested_poles : 1-D ndarray\n                The poles the algorithm was asked to place sorted as above,\n                they may differ from what was achieved.\n            X : 2-D ndarray\n                The transfer matrix such as ``X * diag(poles) = (A - B*K)*X``\n                (see Notes)\n            rtol : float\n                The relative tolerance achieved on ``det(X)`` (see Notes).\n                `rtol` will be NaN if it is possible to solve the system\n                ``diag(poles) = (A - B*K)``, or 0 when the optimization\n                algorithms can\'t do anything i.e when ``B.shape[1] == 1``.\n            nb_iter : int\n                The number of iterations performed before converging.\n                `nb_iter` will be NaN if it is possible to solve the system\n                ``diag(poles) = (A - B*K)``, or 0 when the optimization\n                algorithms can\'t do anything i.e when ``B.shape[1] == 1``.\n\n    Notes\n    -----\n    The Tits and Yang (YT), [2]_ paper is an update of the original Kautsky et\n    al. (KNV) paper [1]_.  KNV relies on rank-1 updates to find the transfer\n    matrix X such that ``X * diag(poles) = (A - B*K)*X``, whereas YT uses\n    rank-2 updates. This yields on average more robust solutions (see [2]_\n    pp 21-22), furthermore the YT algorithm supports complex poles whereas KNV\n    does not in its original version.  Only update method 0 proposed by KNV has\n    been implemented here, hence the name ``\'KNV0\'``.\n\n    KNV extended to complex poles is used in Matlab\'s ``place`` function, YT is\n    distributed under a non-free licence by Slicot under the name ``robpole``.\n    It is unclear and undocumented how KNV0 has been extended to complex poles\n    (Tits and Yang claim on page 14 of their paper that their method can not be\n    used to extend KNV to complex poles), therefore only YT supports them in\n    this implementation.\n\n    As the solution to the problem of pole placement is not unique for MIMO\n    systems, both methods start with a tentative transfer matrix which is\n    altered in various way to increase its determinant.  Both methods have been\n    proven to converge to a stable solution, however depending on the way the\n    initial transfer matrix is chosen they will converge to different\n    solutions and therefore there is absolutely no guarantee that using\n    ``\'KNV0\'`` will yield results similar to Matlab\'s or any other\n    implementation of these algorithms.\n\n    Using the default method ``\'YT\'`` should be fine in most cases; ``\'KNV0\'``\n    is only provided because it is needed by ``\'YT\'`` in some specific cases.\n    Furthermore ``\'YT\'`` gives on average more robust results than ``\'KNV0\'``\n    when ``abs(det(X))`` is used as a robustness indicator.\n\n    [2]_ is available as a technical report on the following URL:\n    https://hdl.handle.net/1903/5598\n\n    References\n    ----------\n    .. [1] J. Kautsky, N.K. Nichols and P. van Dooren, "Robust pole assignment\n           in linear state feedback", International Journal of Control, Vol. 41\n           pp. 1129-1155, 1985.\n    .. [2] A.L. Tits and Y. Yang, "Globally convergent algorithms for robust\n           pole assignment by state feedback, IEEE Transactions on Automatic\n           Control, Vol. 41, pp. 1432-1452, 1996.\n\n    Examples\n    --------\n    A simple example demonstrating real pole placement using both KNV and YT\n    algorithms.  This is example number 1 from section 4 of the reference KNV\n    publication ([1]_):\n\n    >>> from scipy import signal\n    >>> import matplotlib.pyplot as plt\n\n    >>> A = np.array([[ 1.380,  -0.2077,  6.715, -5.676  ],\n    ...               [-0.5814, -4.290,   0,      0.6750 ],\n    ...               [ 1.067,   4.273,  -6.654,  5.893  ],\n    ...               [ 0.0480,  4.273,   1.343, -2.104  ]])\n    >>> B = np.array([[ 0,      5.679 ],\n    ...               [ 1.136,  1.136 ],\n    ...               [ 0,      0,    ],\n    ...               [-3.146,  0     ]])\n    >>> P = np.array([-0.2, -0.5, -5.0566, -8.6659])\n\n    Now compute K with KNV method 0, with the default YT method and with the YT\n    method while forcing 100 iterations of the algorithm and print some results\n    after each call.\n\n    >>> fsf1 = signal.place_poles(A, B, P, method=\'KNV0\')\n    >>> fsf1.gain_matrix\n    array([[ 0.20071427, -0.96665799,  0.24066128, -0.10279785],\n           [ 0.50587268,  0.57779091,  0.51795763, -0.41991442]])\n\n    >>> fsf2 = signal.place_poles(A, B, P)  # uses YT method\n    >>> fsf2.computed_poles\n    array([-8.6659, -5.0566, -0.5   , -0.2   ])\n\n    >>> fsf3 = signal.place_poles(A, B, P, rtol=-1, maxiter=100)\n    >>> fsf3.X\n    array([[ 0.52072442+0.j, -0.08409372+0.j, -0.56847937+0.j,  0.74823657+0.j],\n           [-0.04977751+0.j, -0.80872954+0.j,  0.13566234+0.j, -0.29322906+0.j],\n           [-0.82266932+0.j, -0.19168026+0.j, -0.56348322+0.j, -0.43815060+0.j],\n           [ 0.22267347+0.j,  0.54967577+0.j, -0.58387806+0.j, -0.40271926+0.j]])\n\n    The absolute value of the determinant of X is a good indicator to check the\n    robustness of the results, both ``\'KNV0\'`` and ``\'YT\'`` aim at maximizing\n    it.  Below a comparison of the robustness of the results above:\n\n    >>> abs(np.linalg.det(fsf1.X)) < abs(np.linalg.det(fsf2.X))\n    True\n    >>> abs(np.linalg.det(fsf2.X)) < abs(np.linalg.det(fsf3.X))\n    True\n\n    Now a simple example for complex poles:\n\n    >>> A = np.array([[ 0,  7/3.,  0,   0   ],\n    ...               [ 0,   0,    0,  7/9. ],\n    ...               [ 0,   0,    0,   0   ],\n    ...               [ 0,   0,    0,   0   ]])\n    >>> B = np.array([[ 0,  0 ],\n    ...               [ 0,  0 ],\n    ...               [ 1,  0 ],\n    ...               [ 0,  1 ]])\n    >>> P = np.array([-3, -1, -2-1j, -2+1j]) / 3.\n    >>> fsf = signal.place_poles(A, B, P, method=\'YT\')\n\n    We can plot the desired and computed poles in the complex plane:\n\n    >>> t = np.linspace(0, 2*np.pi, 401)\n    >>> plt.plot(np.cos(t), np.sin(t), \'k--\')  # unit circle\n    >>> plt.plot(fsf.requested_poles.real, fsf.requested_poles.imag,\n    ...          \'wo\', label=\'Desired\')\n    >>> plt.plot(fsf.computed_poles.real, fsf.computed_poles.imag, \'bx\',\n    ...          label=\'Placed\')\n    >>> plt.grid()\n    >>> plt.axis(\'image\')\n    >>> plt.axis([-1.1, 1.1, -1.1, 1.1])\n    >>> plt.legend(bbox_to_anchor=(1.05, 1), loc=2, numpoints=1)\n\n    '
    (update_loop, poles) = _valid_inputs(A, B, poles, method, rtol, maxiter)
    cur_rtol = 0
    nb_iter = 0
    (u, z) = s_qr(B, mode='full')
    rankB = np.linalg.matrix_rank(B)
    u0 = u[:, :rankB]
    u1 = u[:, rankB:]
    z = z[:rankB, :]
    if (B.shape[0] == rankB):
        diag_poles = np.zeros(A.shape)
        idx = 0
        while (idx < poles.shape[0]):
            p = poles[idx]
            diag_poles[(idx, idx)] = np.real(p)
            if (~ np.isreal(p)):
                diag_poles[(idx, (idx + 1))] = (- np.imag(p))
                diag_poles[((idx + 1), (idx + 1))] = np.real(p)
                diag_poles[((idx + 1), idx)] = np.imag(p)
                idx += 1
            idx += 1
        gain_matrix = np.linalg.lstsq(B, (diag_poles - A), rcond=(- 1))[0]
        transfer_matrix = np.eye(A.shape[0])
        cur_rtol = np.nan
        nb_iter = np.nan
    else:
        ker_pole = []
        skip_conjugate = False
        for j in range(B.shape[0]):
            if skip_conjugate:
                skip_conjugate = False
                continue
            pole_space_j = np.dot(u1.T, (A - (poles[j] * np.eye(B.shape[0])))).T
            (Q, _) = s_qr(pole_space_j, mode='full')
            ker_pole_j = Q[:, pole_space_j.shape[1]:]
            transfer_matrix_j = np.sum(ker_pole_j, axis=1)[:, np.newaxis]
            transfer_matrix_j = (transfer_matrix_j / np.linalg.norm(transfer_matrix_j))
            if (~ np.isreal(poles[j])):
                transfer_matrix_j = np.hstack([np.real(transfer_matrix_j), np.imag(transfer_matrix_j)])
                ker_pole.extend([ker_pole_j, ker_pole_j])
                skip_conjugate = True
            else:
                ker_pole.append(ker_pole_j)
            if (j == 0):
                transfer_matrix = transfer_matrix_j
            else:
                transfer_matrix = np.hstack((transfer_matrix, transfer_matrix_j))
        if (rankB > 1):
            (stop, cur_rtol, nb_iter) = update_loop(ker_pole, transfer_matrix, poles, B, maxiter, rtol)
            if ((not stop) and (rtol > 0)):
                err_msg = ('Convergence was not reached after maxiter iterations.\nYou asked for a relative tolerance of %f we got %f' % (rtol, cur_rtol))
                warnings.warn(err_msg)
        transfer_matrix = transfer_matrix.astype(complex)
        idx = 0
        while (idx < (poles.shape[0] - 1)):
            if (~ np.isreal(poles[idx])):
                rel = transfer_matrix[:, idx].copy()
                img = transfer_matrix[:, (idx + 1)]
                transfer_matrix[:, idx] = (rel - (1j * img))
                transfer_matrix[:, (idx + 1)] = (rel + (1j * img))
                idx += 1
            idx += 1
        try:
            m = np.linalg.solve(transfer_matrix.T, np.dot(np.diag(poles), transfer_matrix.T)).T
            gain_matrix = np.linalg.solve(z, np.dot(u0.T, (m - A)))
        except np.linalg.LinAlgError:
            raise ValueError("The poles you've chosen can't be placed. Check the controllability matrix and try another set of poles")
    gain_matrix = (- gain_matrix)
    gain_matrix = np.real(gain_matrix)
    full_state_feedback = Bunch()
    full_state_feedback.gain_matrix = gain_matrix
    full_state_feedback.computed_poles = _order_complex_poles(np.linalg.eig((A - np.dot(B, gain_matrix)))[0])
    full_state_feedback.requested_poles = poles
    full_state_feedback.X = transfer_matrix
    full_state_feedback.rtol = cur_rtol
    full_state_feedback.nb_iter = nb_iter
    return full_state_feedback