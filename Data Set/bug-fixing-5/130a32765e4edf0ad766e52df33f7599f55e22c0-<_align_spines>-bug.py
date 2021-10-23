def _align_spines(fig, gs):
    '\n    - Align right/left and bottom/top spines of appropriate subplots.\n    - Compare size of subplotspec including height and width ratios\n       and make sure that the axes spines are at least as large\n       as they should be.\n    '
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
        (rownummin[n], colnummin[n]) = divmod(ss0.num1, ncols)
        (rownummax[n], colnummax[n]) = divmod(ss0.num2, ncols)
        width[n] = np.sum(width_ratios[colnummin[n]:(colnummax[n] + 1)])
        height[n] = np.sum(height_ratios[rownummin[n]:(rownummax[n] + 1)])
    for (nn, ax) in enumerate(axs[:(- 1)]):
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
            elif _in_same_column(colnum0min, colnum0max, colnumCmin, colnumCmax):
                if (height0 > heightC):
                    ax._poslayoutbox.constrain_height_min(((axc._poslayoutbox.height * height0) / heightC))
                    axc._poslayoutbox.constrain_height_min(((ax._poslayoutbox.height * heightC) / (height0 * 1.8)))
                elif (height0 < heightC):
                    axc._poslayoutbox.constrain_height_min(((ax._poslayoutbox.height * heightC) / height0))
                    ax._poslayoutbox.constrain_height_min(((ax._poslayoutbox.height * height0) / (heightC * 1.8)))
            if ((not alignwidth) and (dcols0 == dcolsC)):
                ax._poslayoutbox.constrain_width(((axc._poslayoutbox.width * width0) / widthC))
                alignwidth = True
            elif _in_same_row(rownum0min, rownum0max, rownumCmin, rownumCmax):
                if (width0 > widthC):
                    ax._poslayoutbox.constrain_width_min(((axc._poslayoutbox.width * width0) / widthC))
                    axc._poslayoutbox.constrain_width_min(((ax._poslayoutbox.width * widthC) / (width0 * 1.8)))
                elif (width0 < widthC):
                    axc._poslayoutbox.constrain_width_min(((ax._poslayoutbox.width * widthC) / width0))
                    ax._poslayoutbox.constrain_width_min(((axc._poslayoutbox.width * width0) / (widthC * 1.8)))