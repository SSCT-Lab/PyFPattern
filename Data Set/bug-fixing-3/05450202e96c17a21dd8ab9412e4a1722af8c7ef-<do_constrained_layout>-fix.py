def do_constrained_layout(fig, renderer, h_pad, w_pad, hspace=None, wspace=None):
    '\n    Do the constrained_layout.  Called at draw time in\n     ``figure.constrained_layout()``\n\n    Parameters\n    ----------\n\n\n    fig: Figure\n      is the ``figure`` instance to do the layout in.\n\n    renderer: Renderer\n      the renderer to use.\n\n     h_pad, w_pad : float\n       are in figure-normalized units, and are a padding around the axes\n       elements.\n\n     hspace, wspace : float\n        are in fractions of the subplot sizes.\n\n    '
    "  Steps:\n\n    1. get a list of unique gridspecs in this figure.  Each gridspec will be\n    constrained separately.\n    2. Check for gaps in the gridspecs.  i.e. if not every axes slot in the\n    gridspec has been filled.  If empty, add a ghost axis that is made so\n    that it cannot be seen (though visible=True).  This is needed to make\n    a blank spot in the layout.\n    3. Compare the tight_bbox of each axes to its `position`, and assume that\n    the difference is the space needed by the elements around the edge of\n    the axes (decorations) like the title, ticklabels, x-labels, etc.  This\n    can include legends who overspill the axes boundaries.\n    4. Constrain gridspec elements to line up:\n        a) if colnum0 neq colnumC, the two subplotspecs are stacked next to\n        each other, with the appropriate order.\n        b) if colnum0 == columnC line up the left or right side of the\n        _poslayoutbox (depending if it is the min or max num that is equal).\n        c) do the same for rows...\n    5. The above doesn't constrain relative sizes of the _poslayoutboxes at\n    all, and indeed zero-size is a solution that the solver often finds more\n    convenient than expanding the sizes.  Right now the solution is to compare\n    subplotspec sizes (i.e. drowsC and drows0) and constrain the larger\n    _poslayoutbox to be larger than the ratio of the sizes.  i.e. if drows0 >\n    drowsC,  then ax._poslayoutbox > axc._poslayoutbox * drowsC / drows0. This\n    works fine *if* the decorations are similar between the axes.  If the\n    larger subplotspec has much larger axes decorations, then the constraint\n    above is incorrect.\n\n    We need the greater than in the above, in general, rather than an equals\n    sign.  Consider the case of the left column having 2 rows, and the right\n    column having 1 row.  We want the top and bottom of the _poslayoutboxes to\n    line up. So that means if there are decorations on the left column axes\n    they will be smaller than half as large as the right hand axis.\n\n    This can break down if the decoration size for the right hand axis (the\n    margins) is very large.  There must be a math way to check for this case.\n\n    "
    try:
        if (fig.canvas.toolbar._active in ('PAN', 'ZOOM')):
            return
    except AttributeError:
        pass
    invTransFig = fig.transFigure.inverted().transform_bbox
    gss = set()
    for ax in fig.axes:
        if hasattr(ax, 'get_subplotspec'):
            gs = ax.get_subplotspec().get_gridspec()
            if (gs._layoutbox is not None):
                gss.add(gs)
    if (len(gss) == 0):
        warnings.warn('There are no gridspecs with layoutboxes. Possibly did not call parent GridSpec with the figure= keyword')
    if (fig._layoutbox.constrained_layout_called < 1):
        for gs in gss:
            _make_ghost_gridspec_slots(fig, gs)
    for nnn in range(2):
        for ax in fig.axes:
            _log.debug(ax._layoutbox)
            if (ax._layoutbox is not None):
                _make_layout_margins(ax, renderer, h_pad, w_pad)
        if ((fig._suptitle is not None) and (fig._suptitle._layoutbox is not None)):
            sup = fig._suptitle
            bbox = invTransFig(sup.get_window_extent(renderer=renderer))
            height = (bbox.y1 - bbox.y0)
            sup._layoutbox.edit_height((height + h_pad))
        if (fig._layoutbox.constrained_layout_called < 1):
            figlb = fig._layoutbox
            for child in figlb.children:
                if child._is_gridspec_layoutbox():
                    _arrange_subplotspecs(child, hspace=hspace, wspace=wspace)
            for gs in gss:
                _align_spines(fig, gs)
        fig._layoutbox.constrained_layout_called += 1
        fig._layoutbox.update_variables()
        if _axes_all_finite_sized(fig):
            for ax in fig.axes:
                if (ax._layoutbox is not None):
                    newpos = ax._poslayoutbox.get_rect()
                    ax._set_position(newpos, which='original')
        else:
            warnings.warn('constrained_layout not applied.  At least one axes collapsed to zero width or height.')