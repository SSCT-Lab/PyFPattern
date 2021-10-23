def dendrogram(Z, p=30, truncate_mode=None, color_threshold=None, get_leaves=True, orientation='top', labels=None, count_sort=False, distance_sort=False, show_leaf_counts=True, no_plot=False, no_labels=False, leaf_font_size=None, leaf_rotation=None, leaf_label_func=None, show_contracted=False, link_color_func=None, ax=None, above_threshold_color='b'):
    "\n    Plots the hierarchical clustering as a dendrogram.\n\n    The dendrogram illustrates how each cluster is\n    composed by drawing a U-shaped link between a non-singleton\n    cluster and its children. The height of the top of the U-link is\n    the distance between its children clusters. It is also the\n    cophenetic distance between original observations in the two\n    children clusters. It is expected that the distances in Z[:,2] be\n    monotonic, otherwise crossings appear in the dendrogram.\n\n    Parameters\n    ----------\n    Z : ndarray\n        The linkage matrix encoding the hierarchical clustering to\n        render as a dendrogram. See the ``linkage`` function for more\n        information on the format of ``Z``.\n    p : int, optional\n        The ``p`` parameter for ``truncate_mode``.\n    truncate_mode : str, optional\n        The dendrogram can be hard to read when the original\n        observation matrix from which the linkage is derived is\n        large. Truncation is used to condense the dendrogram. There\n        are several modes:\n\n        ``None/'none'``\n          No truncation is performed (Default).\n\n        ``'lastp'``\n          The last ``p`` non-singleton formed in the linkage are the only\n          non-leaf nodes in the linkage; they correspond to rows\n          ``Z[n-p-2:end]`` in ``Z``. All other non-singleton clusters are\n          contracted into leaf nodes.\n\n        ``'mlab'``\n          This corresponds to MATLAB(TM) behavior. (not implemented yet)\n\n        ``'level'/'mtica'``\n          No more than ``p`` levels of the dendrogram tree are displayed.\n          This corresponds to Mathematica(TM) behavior.\n\n    color_threshold : double, optional\n        For brevity, let :math:`t` be the ``color_threshold``.\n        Colors all the descendent links below a cluster node\n        :math:`k` the same color if :math:`k` is the first node below\n        the cut threshold :math:`t`. All links connecting nodes with\n        distances greater than or equal to the threshold are colored\n        blue. If :math:`t` is less than or equal to zero, all nodes\n        are colored blue. If ``color_threshold`` is None or\n        'default', corresponding with MATLAB(TM) behavior, the\n        threshold is set to ``0.7*max(Z[:,2])``.\n    get_leaves : bool, optional\n        Includes a list ``R['leaves']=H`` in the result\n        dictionary. For each :math:`i`, ``H[i] == j``, cluster node\n        ``j`` appears in position ``i`` in the left-to-right traversal\n        of the leaves, where :math:`j < 2n-1` and :math:`i < n`.\n    orientation : str, optional\n        The direction to plot the dendrogram, which can be any\n        of the following strings:\n\n        ``'top'``\n          Plots the root at the top, and plot descendent links going downwards.\n          (default).\n\n        ``'bottom'``\n          Plots the root at the bottom, and plot descendent links going\n          upwards.\n\n        ``'left'``\n          Plots the root at the left, and plot descendent links going right.\n\n        ``'right'``\n          Plots the root at the right, and plot descendent links going left.\n\n    labels : ndarray, optional\n        By default ``labels`` is None so the index of the original observation\n        is used to label the leaf nodes.  Otherwise, this is an :math:`n`\n        -sized list (or tuple). The ``labels[i]`` value is the text to put\n        under the :math:`i` th leaf node only if it corresponds to an original\n        observation and not a non-singleton cluster.\n    count_sort : str or bool, optional\n        For each node n, the order (visually, from left-to-right) n's\n        two descendent links are plotted is determined by this\n        parameter, which can be any of the following values:\n\n        ``False``\n          Nothing is done.\n\n        ``'ascending'`` or ``True``\n          The child with the minimum number of original objects in its cluster\n          is plotted first.\n\n        ``'descendent'``\n          The child with the maximum number of original objects in its cluster\n          is plotted first.\n\n        Note ``distance_sort`` and ``count_sort`` cannot both be True.\n    distance_sort : str or bool, optional\n        For each node n, the order (visually, from left-to-right) n's\n        two descendent links are plotted is determined by this\n        parameter, which can be any of the following values:\n\n        ``False``\n          Nothing is done.\n\n        ``'ascending'`` or ``True``\n          The child with the minimum distance between its direct descendents is\n          plotted first.\n\n        ``'descending'``\n          The child with the maximum distance between its direct descendents is\n          plotted first.\n\n        Note ``distance_sort`` and ``count_sort`` cannot both be True.\n    show_leaf_counts : bool, optional\n         When True, leaf nodes representing :math:`k>1` original\n         observation are labeled with the number of observations they\n         contain in parentheses.\n    no_plot : bool, optional\n        When True, the final rendering is not performed. This is\n        useful if only the data structures computed for the rendering\n        are needed or if matplotlib is not available.\n    no_labels : bool, optional\n        When True, no labels appear next to the leaf nodes in the\n        rendering of the dendrogram.\n    leaf_rotation : double, optional\n        Specifies the angle (in degrees) to rotate the leaf\n        labels. When unspecified, the rotation is based on the number of\n        nodes in the dendrogram (default is 0).\n    leaf_font_size : int, optional\n        Specifies the font size (in points) of the leaf labels. When\n        unspecified, the size based on the number of nodes in the\n        dendrogram.\n    leaf_label_func : lambda or function, optional\n        When leaf_label_func is a callable function, for each\n        leaf with cluster index :math:`k < 2n-1`. The function\n        is expected to return a string with the label for the\n        leaf.\n\n        Indices :math:`k < n` correspond to original observations\n        while indices :math:`k \\geq n` correspond to non-singleton\n        clusters.\n\n        For example, to label singletons with their node id and\n        non-singletons with their id, count, and inconsistency\n        coefficient, simply do::\n\n            # First define the leaf label function.\n            def llf(id):\n                if id < n:\n                    return str(id)\n                else:\n                    return '[%d %d %1.2f]' % (id, count, R[n-id,3])\n            # The text for the leaf nodes is going to be big so force\n            # a rotation of 90 degrees.\n            dendrogram(Z, leaf_label_func=llf, leaf_rotation=90)\n\n    show_contracted : bool, optional\n        When True the heights of non-singleton nodes contracted\n        into a leaf node are plotted as crosses along the link\n        connecting that leaf node.  This really is only useful when\n        truncation is used (see ``truncate_mode`` parameter).\n    link_color_func : callable, optional\n        If given, `link_color_function` is called with each non-singleton id\n        corresponding to each U-shaped link it will paint. The function is\n        expected to return the color to paint the link, encoded as a matplotlib\n        color string code. For example::\n\n            dendrogram(Z, link_color_func=lambda k: colors[k])\n\n        colors the direct links below each untruncated non-singleton node\n        ``k`` using ``colors[k]``.\n    ax : matplotlib Axes instance, optional\n        If None and `no_plot` is not True, the dendrogram will be plotted\n        on the current axes.  Otherwise if `no_plot` is not True the\n        dendrogram will be plotted on the given ``Axes`` instance. This can be\n        useful if the dendrogram is part of a more complex figure.\n    above_threshold_color : str, optional\n        This matplotlib color string sets the color of the links above the\n        color_threshold. The default is 'b'.\n\n    Returns\n    -------\n    R : dict\n        A dictionary of data structures computed to render the\n        dendrogram. Its has the following keys:\n\n        ``'color_list'``\n          A list of color names. The k'th element represents the color of the\n          k'th link.\n\n        ``'icoord'`` and ``'dcoord'``\n          Each of them is a list of lists. Let ``icoord = [I1, I2, ..., Ip]``\n          where ``Ik = [xk1, xk2, xk3, xk4]`` and ``dcoord = [D1, D2, ..., Dp]``\n          where ``Dk = [yk1, yk2, yk3, yk4]``, then the k'th link painted is\n          ``(xk1, yk1)`` - ``(xk2, yk2)`` - ``(xk3, yk3)`` - ``(xk4, yk4)``.\n\n        ``'ivl'``\n          A list of labels corresponding to the leaf nodes.\n\n        ``'leaves'``\n          For each i, ``H[i] == j``, cluster node ``j`` appears in position\n          ``i`` in the left-to-right traversal of the leaves, where\n          :math:`j < 2n-1` and :math:`i < n`. If ``j`` is less than ``n``, the\n          ``i``-th leaf node corresponds to an original observation.\n          Otherwise, it corresponds to a non-singleton cluster.\n\n    See Also\n    --------\n    linkage, set_link_color_palette\n\n    Examples\n    --------\n    >>> from scipy.cluster import hierarchy\n    >>> import matplotlib.pyplot as plt\n\n    A very basic example:\n\n    >>> ytdist = np.array([662., 877., 255., 412., 996., 295., 468., 268.,\n    ...                    400., 754., 564., 138., 219., 869., 669.])\n    >>> Z = hierarchy.linkage(ytdist, 'single')\n    >>> plt.figure()\n    >>> dn = hierarchy.dendrogram(Z)\n\n    Now plot in given axes, improve the color scheme and use both vertical and\n    horizontal orientations:\n\n    >>> hierarchy.set_link_color_palette(['m', 'c', 'y', 'k'])\n    >>> fig, axes = plt.subplots(1, 2, figsize=(8, 3))\n    >>> dn1 = hierarchy.dendrogram(Z, ax=axes[0], above_threshold_color='y',\n    ...                            orientation='top')\n    >>> dn2 = hierarchy.dendrogram(Z, ax=axes[1], above_threshold_color='#bcbddc',\n    ...                            orientation='right')\n    >>> hierarchy.set_link_color_palette(None)  # reset to default after use\n    >>> plt.show()\n\n    "
    Z = np.asarray(Z, order='c')
    if (orientation not in ['top', 'left', 'bottom', 'right']):
        raise ValueError("orientation must be one of 'top', 'left', 'bottom', or 'right'")
    is_valid_linkage(Z, throw=True, name='Z')
    Zs = Z.shape
    n = (Zs[0] + 1)
    if (type(p) in (int, float)):
        p = int(p)
    else:
        raise TypeError('The second argument must be a number')
    if (truncate_mode not in ('lastp', 'mlab', 'mtica', 'level', 'none', None)):
        raise ValueError('Invalid truncation mode.')
    if ((truncate_mode == 'lastp') or (truncate_mode == 'mlab')):
        if ((p > n) or (p == 0)):
            p = n
    if ((truncate_mode == 'mtica') or (truncate_mode == 'level')):
        if (p <= 0):
            p = np.inf
    if get_leaves:
        lvs = []
    else:
        lvs = None
    icoord_list = []
    dcoord_list = []
    color_list = []
    current_color = [0]
    currently_below_threshold = [False]
    ivl = []
    if ((color_threshold is None) or (isinstance(color_threshold, string_types) and (color_threshold == 'default'))):
        color_threshold = (max(Z[:, 2]) * 0.7)
    R = {
        'icoord': icoord_list,
        'dcoord': dcoord_list,
        'ivl': ivl,
        'leaves': lvs,
        'color_list': color_list,
    }
    contraction_marks = ([] if show_contracted else None)
    _dendrogram_calculate_info(Z=Z, p=p, truncate_mode=truncate_mode, color_threshold=color_threshold, get_leaves=get_leaves, orientation=orientation, labels=labels, count_sort=count_sort, distance_sort=distance_sort, show_leaf_counts=show_leaf_counts, i=((2 * n) - 2), iv=0.0, ivl=ivl, n=n, icoord_list=icoord_list, dcoord_list=dcoord_list, lvs=lvs, current_color=current_color, color_list=color_list, currently_below_threshold=currently_below_threshold, leaf_label_func=leaf_label_func, contraction_marks=contraction_marks, link_color_func=link_color_func, above_threshold_color=above_threshold_color)
    if (not no_plot):
        mh = max(Z[:, 2])
        _plot_dendrogram(icoord_list, dcoord_list, ivl, p, n, mh, orientation, no_labels, color_list, leaf_font_size=leaf_font_size, leaf_rotation=leaf_rotation, contraction_marks=contraction_marks, ax=ax, above_threshold_color=above_threshold_color)
    return R