def cycle_spin(x, func, max_shifts, shift_steps=1, num_workers=None, multichannel=False, func_kw={
    
}):
    'Cycle spinning (repeatedly apply func to shifted versions of x).\n\n    Parameters\n    ----------\n    x : array-like\n        Data for input to ``func``.\n    func : function\n        A function to apply to circularly shifted versions of ``x``.  Should\n        take ``x`` as its first argument. Any additional arguments can be\n        supplied via ``func_kw``.\n    max_shifts : int or tuple\n        If an integer, shifts in ``range(0, max_shifts+1)`` will be used along\n        each axis of ``x``. If a tuple, ``range(0, max_shifts[i]+1)`` will be\n        along axis i.\n    shift_steps : int or tuple, optional\n        The step size for the shifts applied along axis, i, are::\n        ``range((0, max_shifts[i]+1, shift_steps[i]))``. If an integer is\n        provided, the same step size is used for all axes.\n    num_workers : int or None, optional\n        The number of parallel threads to use during cycle spinning. If set to\n        ``None``, the full set of available cores are used.\n    multichannel : bool, optional\n        Whether to treat the final axis as channels (no cycle shifts are\n        performed over the channels axis).\n    func_kw : dict, optional\n        Additional keyword arguments to supply to ``func``.\n\n    Returns\n    -------\n    avg_y : np.ndarray\n        The output of ``func(x, **func_kw)`` averaged over all combinations of\n        the specified axis shifts.\n\n    Notes\n    -----\n    Cycle spinning was proposed as a way to approach shift-invariance via\n    performing several circular shifts of a shift-variant transform [1]_.\n\n    For a n-level discrete wavelet transforms, one may wish to perform all\n    shifts up to ``max_shifts = 2**n - 1``. In practice, much of the benefit\n    can often be realized with only a small number of shifts per axis.\n\n    For transforms such as the blockwise discrete cosine transform, one may\n    wish to evaluate shifts up to the block size used by the transform.\n\n    References\n    ----------\n    .. [1] R.R. Coifman and D.L. Donoho.  "Translation-Invariant De-Noising".\n           Wavelets and Statistics, Lecture Notes in Statistics, vol.103.\n           Springer, New York, 1995, pp.125-150.\n           DOI:10.1007/978-1-4612-2544-7_9\n\n    Examples\n    --------\n    >>> import skimage.data\n    >>> from skimage import img_as_float\n    >>> from skimage.restoration import denoise_wavelet, cycle_spin\n    >>> img = img_as_float(skimage.data.camera())\n    >>> sigma = 0.1\n    >>> img = img + sigma * np.random.standard_normal(img.shape)\n    >>> denoised = cycle_spin(img, func=denoise_wavelet, max_shifts=3)\n\n    '
    x = np.asanyarray(x)
    all_shifts = _generate_shifts(x.ndim, multichannel, max_shifts, shift_steps)
    all_shifts = list(all_shifts)

    def _run_one_shift(shift):
        xs = _roll_axes(x, shift)
        tmp = func(xs, **func_kw)
        return _roll_axes(tmp, (- np.asarray(shift)))
    if (num_workers == 1):
        mean = _run_one_shift(all_shifts[0])
        for shift in all_shifts[1:]:
            mean += _run_one_shift(shift)
        mean /= len(all_shifts)
    else:
        futures = [dask.delayed(_run_one_shift)(s) for s in all_shifts]
        mean = (sum(futures) / len(futures))
        mean = mean.compute(num_workers=num_workers)
    return mean