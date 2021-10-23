def _raise_build_error(e):
    local_dir = osp.split(__file__)[0]
    msg = _STANDARD_MSG
    if (local_dir == 'skimage'):
        msg = _INPLACE_MSG
    raise ImportError(('%s\nIt seems that scikit-image has not been built correctly.\n%s' % (e, msg)))