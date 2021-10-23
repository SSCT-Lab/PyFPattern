def do_constrained_layout(fig, renderer, h_pad, w_pad, hspace=None, wspace=None):
    '\n    Do the constrained_layout.  Called at draw time in\n     ``figure.constrained_layout()``\n\n    Parameters\n    ----------\n\n\n    fig: Figure\n      is the ``figure`` instance to do the layout in.\n\n    renderer: Renderer\n      the renderer to use.\n\n     h_pad, w_pad : float\n       are in figure-normalized units, and are a padding around the axes\n       elements.\n\n     hspace, wspace : float\n        are in fractions of the subplot sizes.\n\n    '
    "  Steps:\n\n    1. get a list of unique gridspecs in this figure.  Each gridspec will be\n    constrained separately.\n    2. Check for gaps in the gridspecs.  i.e. if not every axes slot in the\n    gridspec has been filled.  If empty, add a ghost axis that is made so\n    that it cannot be seen (though visible=True).  This is needed to make\n    a blank spot in the layout.\n    3. Compare the tight_bbox of each axes to its `position`, and assume that\n    the difference is the space needed by the elements around the edge of\n    the axes (decorations) like the title, ticklabels, x-labels, etc.  This\n    can include legends who overspill the axes boundaries.\n    4. Constrain gridspec elements to line up:\n        a) if colnum0 neq colnumC, the two subplotspecs are stacked next to\n        each other, with the appropriate order.\n        b) if colnum0 == columnC line up the left or right side of the\n        _poslayoutbox (depending if it is the min or max num that is equal).\n        c) do the same for rows...\n    5. The above doesn't constrain relative sizes of the _poslayoutboxes at\n    all, and indeed zero-size is a solution that the solver often finds more\n    convenient than expanding the sizes.  Right now the solution is to compare\n    subplotspec sizes (i.e. drowsC and drows0) and constrain the larger\n    _poslayoutbox to be larger than the ratio of the sizes.  i.e. if drows0 >\n    drowsC,  then ax._poslayoutbox > axc._poslayoutbox * drowsC / drows0. This\n    works fine *if* the decorations are similar between the axes.  If the\n    larger subplotspec has much larger axes decorations, then the constraint\n    above is incorrect.\n\n    We need the greater than in the above, in general, rather than an equals\n    sign.  Consider the case of the left column having 2 rows, and the right\n    column having 1 row.  We want the top and bottom of the _poslayoutboxes to\n    line up. So that means if there are decorations on the left column axes\n    they will be smaller than half as large as the right hand axis.\n\n    This can break down if the decoration size for the right hand axis (the\n    margins) is very large.  There must be a math way to check for this case.\n\n    "
    invTransFig = fig.transFigure.inverted().transform_bbox
    gss = set([])
    for ax in fig.axes:
        if hasattr(ax, 'get_subplotspec'):
            gs = ax.get_subplotspec().get_gridspec()
            if (gs._layoutbox is not None):
                gss.add(gs)
    if (len(gss) == 0):
        warnings.warn('There are no gridspecs with layoutboxes. Possibly did not call parent GridSpec with the figure= keyword')
    if (fig._layoutbox.constrained_layout_called < 1):
        for gs in gss:
            (nrows, ncols) = gs.get_geometry()
            hassubplotspec = np.zeros((nrows * ncols), dtype=bool)
            axs = []
            for ax in fig.axes:
                if (hasattr(ax, 'get_subplotspec') and (ax._layoutbox is not None) and (ax.get_subplotspec().get_gridspec() == gs)):
                    axs += [ax]
            for ax in axs:
                ss0 = ax.get_subplotspec()
                if (ss0.num2 is None):
                    ss0.num2 = ss0.num1
                hassubplotspec[ss0.num1:(ss0.num2 + 1)] = True
            for (nn, hss) in enumerate(hassubplotspec):
                if (not hss):
                    ax = fig.add_subplot(gs[nn])
                    ax.set_frame_on(False)
                    ax.set_xticks([])
                    ax.set_yticks([])
                    ax.set_facecolor((1, 0, 0, 0))
    for ax in fig.axes:
        _log.debug(ax._layoutbox)
        if (ax._layoutbox is not None):
            pos = ax.get_position(original=True)
            tightbbox = get_axall_tightbbox(ax, renderer)
            bbox = invTransFig(tightbbox)
            h_padt = ax._poslayoutbox.h_pad
            if (h_padt is None):
                h_padt = h_pad
            w_padt = ax._poslayoutbox.w_pad
            if (w_padt is None):
                w_padt = w_pad
            ax._poslayoutbox.edit_left_margin_min((((- bbox.x0) + pos.x0) + w_padt))
            ax._poslayoutbox.edit_right_margin_min(((bbox.x1 - pos.x1) + w_padt))
            ax._poslayoutbox.edit_bottom_margin_min((((- bbox.y0) + pos.y0) + h_padt))
            ax._poslayoutbox.edit_top_margin_min(((bbox.y1 - pos.y1) + h_padt))
            _log.debug('left %f', (((- bbox.x0) + pos.x0) + w_pad))
            _log.debug('right %f', ((bbox.x1 - pos.x1) + w_pad))
            _log.debug('bottom %f', (((- bbox.y0) + pos.y0) + h_padt))
            if (fig._layoutbox.constrained_layout_called < 1):
                ax._poslayoutbox.constrain_height_min(20, strength='weak')
                ax._poslayoutbox.constrain_width_min(20, strength='weak')
                ax._layoutbox.constrain_height_min(20, strength='weak')
                ax._layoutbox.constrain_width_min(20, strength='weak')
                ax._poslayoutbox.constrain_top_margin(0, strength='weak')
                ax._poslayoutbox.constrain_bottom_margin(0, strength='weak')
                ax._poslayoutbox.constrain_right_margin(0, strength='weak')
                ax._poslayoutbox.constrain_left_margin(0, strength='weak')
    if (fig._suptitle is not None):
        sup = fig._suptitle
        bbox = invTransFig(sup.get_window_extent(renderer=renderer))
        height = (bbox.y1 - bbox.y0)
        sup._layoutbox.edit_height((height + h_pad))
    if (fig._layoutbox.constrained_layout_called < 1):
        figlb = fig._layoutbox
        for child in figlb.children:
            if child._is_gridspec_layoutbox():
                arange_subplotspecs(child, hspace=hspace, wspace=wspace)
        for gs in gss:
            (nrows, ncols) = gs.get_geometry()
            width_ratios = gs.get_width_ratios()
            height_ratios = gs.get_height_ratios()
            if (width_ratios is None):
                width_ratios = np.ones(ncols)
            if (height_ratios is None):
                height_ratios = np.ones(nrows)
            axs = []
            for ax in fig.axes:
                if (hasattr(ax, 'get_subplotspec') and (ax._layoutbox is not None)):
                    if (ax.get_subplotspec().get_gridspec() == gs):
                        axs += [ax]
            rownummin = np.zeros(len(axs), dtype=np.int8)
            rownummax = np.zeros(len(axs), dtype=np.int8)
            colnummin = np.zeros(len(axs), dtype=np.int8)
            colnummax = np.zeros(len(axs), dtype=np.int8)
            width = np.zeros(len(axs))
            height = np.zeros(len(axs))
            for (n, ax) in enumerate(axs):
                ss0 = ax.get_subplotspec()
                if (ss0.num2 is None):
                    ss0.num2 = ss0.num1
                (rownummin[n], colnummin[n]) = divmod(ss0.num1, ncols)
                (rownummax[n], colnummax[n]) = divmod(ss0.num2, ncols)
                width[n] = np.sum(width_ratios[colnummin[n]:(colnummax[n] + 1)])
                height[n] = np.sum(height_ratios[rownummin[n]:(rownummax[n] + 1)])
            for (nn, ax) in enumerate(axs[:(- 1)]):
                ss0 = ax.get_subplotspec()
                (rownum0min, colnum0min) = (rownummin[nn], colnummin[nn])
                (rownum0max, colnum0max) = (rownummax[nn], colnummax[nn])
                (width0, height0) = (width[nn], height[nn])
                alignleft = False
                alignright = False
                alignbot = False
                aligntop = False
                alignheight = False
                alignwidth = False
                for mm in range((nn + 1), len(axs)):
                    axc = axs[mm]
                    (rownumCmin, colnumCmin) = (rownummin[mm], colnummin[mm])
                    (rownumCmax, colnumCmax) = (rownummax[mm], colnummax[mm])
                    (widthC, heightC) = (width[mm], height[mm])
                    if ((not alignleft) and (colnum0min == colnumCmin)):
                        layoutbox.align([ax._poslayoutbox, axc._poslayoutbox], 'left')
                        alignleft = True
                    if ((not alignright) and (colnum0max == colnumCmax)):
                        layoutbox.align([ax._poslayoutbox, axc._poslayoutbox], 'right')
                        alignright = True
                    if ((not aligntop) and (rownum0min == rownumCmin)):
                        _log.debug('rownum0min == rownumCmin')
                        layoutbox.align([ax._poslayoutbox, axc._poslayoutbox], 'top')
                        aligntop = True
                    if ((not alignbot) and (rownum0max == rownumCmax)):
                        _log.debug('rownum0max == rownumCmax')
                        layoutbox.align([ax._poslayoutbox, axc._poslayoutbox], 'bottom')
                        alignbot = True
                    drowsC = ((rownumCmax - rownumCmin) + 1)
                    drows0 = ((rownum0max - rownum0min) + 1)
                    dcolsC = ((colnumCmax - colnumCmin) + 1)
                    dcols0 = ((colnum0max - colnum0min) + 1)
                    if ((not alignheight) and (drows0 == drowsC)):
                        ax._poslayoutbox.constrain_height(((axc._poslayoutbox.height * height0) / heightC))
                        alignheight = True
                    elif in_same_column(colnum0min, colnum0max, colnumCmin, colnumCmax):
                        if (height0 > heightC):
                            ax._poslayoutbox.constrain_height_min(((axc._poslayoutbox.height * height0) / heightC))
                            axc._poslayoutbox.constrain_height_min(((ax._poslayoutbox.height * heightC) / (height0 * 1.8)))
                        elif (height0 < heightC):
                            axc._poslayoutbox.constrain_height_min(((ax._poslayoutbox.height * heightC) / height0))
                            ax._poslayoutbox.constrain_height_min(((ax._poslayoutbox.height * height0) / (heightC * 1.8)))
                    if ((not alignwidth) and (dcols0 == dcolsC)):
                        ax._poslayoutbox.constrain_width(((axc._poslayoutbox.width * width0) / widthC))
                        alignwidth = True
                    elif in_same_row(rownum0min, rownum0max, rownumCmin, rownumCmax):
                        if (width0 > widthC):
                            ax._poslayoutbox.constrain_width_min(((axc._poslayoutbox.width * width0) / widthC))
                            axc._poslayoutbox.constrain_width_min(((ax._poslayoutbox.width * widthC) / (width0 * 1.8)))
                        elif (width0 < widthC):
                            axc._poslayoutbox.constrain_width_min(((ax._poslayoutbox.width * widthC) / width0))
                            ax._poslayoutbox.constrain_width_min(((axc._poslayoutbox.width * width0) / (widthC * 1.8)))
    fig._layoutbox.constrained_layout_called += 1
    fig._layoutbox.update_variables()
    for ax in fig.axes:
        if (ax._layoutbox is not None):
            newpos = ax._poslayoutbox.get_rect()
            _log.debug('newpos %r', newpos)
            ax._set_position(newpos, which='original')