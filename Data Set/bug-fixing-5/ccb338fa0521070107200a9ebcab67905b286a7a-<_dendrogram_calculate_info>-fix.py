def _dendrogram_calculate_info(Z, p, truncate_mode, color_threshold=np.inf, get_leaves=True, orientation='top', labels=None, count_sort=False, distance_sort=False, show_leaf_counts=False, i=(- 1), iv=0.0, ivl=[], n=0, icoord_list=[], dcoord_list=[], lvs=None, mhr=False, current_color=[], color_list=[], currently_below_threshold=[], leaf_label_func=None, level=0, contraction_marks=None, link_color_func=None, above_threshold_color='b'):
    "\n    Calculates the endpoints of the links as well as the labels for the\n    the dendrogram rooted at the node with index i. iv is the independent\n    variable value to plot the left-most leaf node below the root node i\n    (if orientation='top', this would be the left-most x value where the\n    plotting of this root node i and its descendents should begin).\n\n    ivl is a list to store the labels of the leaf nodes. The leaf_label_func\n    is called whenever ivl != None, labels == None, and\n    leaf_label_func != None. When ivl != None and labels != None, the\n    labels list is used only for labeling the leaf nodes. When\n    ivl == None, no labels are generated for leaf nodes.\n\n    When get_leaves==True, a list of leaves is built as they are visited\n    in the dendrogram.\n\n    Returns a tuple with l being the independent variable coordinate that\n    corresponds to the midpoint of cluster to the left of cluster i if\n    i is non-singleton, otherwise the independent coordinate of the leaf\n    node if i is a leaf node.\n\n    Returns\n    -------\n    A tuple (left, w, h, md), where:\n\n      * left is the independent variable coordinate of the center of the\n        the U of the subtree\n\n      * w is the amount of space used for the subtree (in independent\n        variable units)\n\n      * h is the height of the subtree in dependent variable units\n\n      * md is the ``max(Z[*,2]``) for all nodes ``*`` below and including\n        the target node.\n\n    "
    if (n == 0):
        raise ValueError('Invalid singleton cluster count n.')
    if (i == (- 1)):
        raise ValueError('Invalid root cluster index i.')
    if (truncate_mode == 'lastp'):
        if (((2 * n) - p) > i >= n):
            d = Z[((i - n), 2)]
            _append_nonsingleton_leaf_node(Z, p, n, level, lvs, ivl, leaf_label_func, i, labels, show_leaf_counts)
            if (contraction_marks is not None):
                _append_contraction_marks(Z, (iv + 5.0), i, n, contraction_marks)
            return ((iv + 5.0), 10.0, 0.0, d)
        elif (i < n):
            _append_singleton_leaf_node(Z, p, n, level, lvs, ivl, leaf_label_func, i, labels)
            return ((iv + 5.0), 10.0, 0.0, 0.0)
    elif (truncate_mode == 'level'):
        if ((i > n) and (level > p)):
            d = Z[((i - n), 2)]
            _append_nonsingleton_leaf_node(Z, p, n, level, lvs, ivl, leaf_label_func, i, labels, show_leaf_counts)
            if (contraction_marks is not None):
                _append_contraction_marks(Z, (iv + 5.0), i, n, contraction_marks)
            return ((iv + 5.0), 10.0, 0.0, d)
        elif (i < n):
            _append_singleton_leaf_node(Z, p, n, level, lvs, ivl, leaf_label_func, i, labels)
            return ((iv + 5.0), 10.0, 0.0, 0.0)
    elif (truncate_mode in ('mlab',)):
        msg = "Mode 'mlab' is deprecated in scipy 0.19.0 (it never worked)."
        warnings.warn(msg, DeprecationWarning)
    if (i < n):
        _append_singleton_leaf_node(Z, p, n, level, lvs, ivl, leaf_label_func, i, labels)
        return ((iv + 5.0), 10.0, 0.0, 0.0)
    aa = int(Z[((i - n), 0)])
    ab = int(Z[((i - n), 1)])
    if (aa > n):
        na = Z[((aa - n), 3)]
        da = Z[((aa - n), 2)]
    else:
        na = 1
        da = 0.0
    if (ab > n):
        nb = Z[((ab - n), 3)]
        db = Z[((ab - n), 2)]
    else:
        nb = 1
        db = 0.0
    if ((count_sort == 'ascending') or (count_sort == True)):
        if (na > nb):
            ua = ab
            ub = aa
        else:
            ua = aa
            ub = ab
    elif (count_sort == 'descending'):
        if (na > nb):
            ua = aa
            ub = ab
        else:
            ua = ab
            ub = aa
    elif ((distance_sort == 'ascending') or (distance_sort == True)):
        if (da > db):
            ua = ab
            ub = aa
        else:
            ua = aa
            ub = ab
    elif (distance_sort == 'descending'):
        if (da > db):
            ua = aa
            ub = ab
        else:
            ua = ab
            ub = aa
    else:
        ua = aa
        ub = ab
    (uiva, uwa, uah, uamd) = _dendrogram_calculate_info(Z=Z, p=p, truncate_mode=truncate_mode, color_threshold=color_threshold, get_leaves=get_leaves, orientation=orientation, labels=labels, count_sort=count_sort, distance_sort=distance_sort, show_leaf_counts=show_leaf_counts, i=ua, iv=iv, ivl=ivl, n=n, icoord_list=icoord_list, dcoord_list=dcoord_list, lvs=lvs, current_color=current_color, color_list=color_list, currently_below_threshold=currently_below_threshold, leaf_label_func=leaf_label_func, level=(level + 1), contraction_marks=contraction_marks, link_color_func=link_color_func, above_threshold_color=above_threshold_color)
    h = Z[((i - n), 2)]
    if ((h >= color_threshold) or (color_threshold <= 0)):
        c = above_threshold_color
        if currently_below_threshold[0]:
            current_color[0] = ((current_color[0] + 1) % len(_link_line_colors))
        currently_below_threshold[0] = False
    else:
        currently_below_threshold[0] = True
        c = _link_line_colors[current_color[0]]
    (uivb, uwb, ubh, ubmd) = _dendrogram_calculate_info(Z=Z, p=p, truncate_mode=truncate_mode, color_threshold=color_threshold, get_leaves=get_leaves, orientation=orientation, labels=labels, count_sort=count_sort, distance_sort=distance_sort, show_leaf_counts=show_leaf_counts, i=ub, iv=(iv + uwa), ivl=ivl, n=n, icoord_list=icoord_list, dcoord_list=dcoord_list, lvs=lvs, current_color=current_color, color_list=color_list, currently_below_threshold=currently_below_threshold, leaf_label_func=leaf_label_func, level=(level + 1), contraction_marks=contraction_marks, link_color_func=link_color_func, above_threshold_color=above_threshold_color)
    max_dist = max(uamd, ubmd, h)
    icoord_list.append([uiva, uiva, uivb, uivb])
    dcoord_list.append([uah, h, h, ubh])
    if (link_color_func is not None):
        v = link_color_func(int(i))
        if (not isinstance(v, string_types)):
            raise TypeError('link_color_func must return a matplotlib color string!')
        color_list.append(v)
    else:
        color_list.append(c)
    return (((uiva + uivb) / 2), (uwa + uwb), h, max_dist)