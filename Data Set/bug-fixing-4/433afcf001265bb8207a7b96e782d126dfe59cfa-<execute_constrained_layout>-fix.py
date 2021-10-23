def execute_constrained_layout(self, renderer=None):
    '\n        Use ``layoutbox`` to determine pos positions within axes.\n\n        See also set_constrained_layout_pads.\n        '
    from matplotlib._constrained_layout import do_constrained_layout
    _log.debug('Executing constrainedlayout')
    if (self._layoutbox is None):
        warnings.warn('Calling figure.constrained_layout, but figure not setup to do constrained layout.  You either called GridSpec without the fig keyword, you are using plt.subplot, or you need to call figure or subplots with the constrained_layout=True kwarg.')
        return
    (w_pad, h_pad, wspace, hspace) = self.get_constrained_layout_pads()
    fig = self
    (width, height) = fig.get_size_inches()
    w_pad = (w_pad / width)
    h_pad = (h_pad / height)
    if (renderer is None):
        renderer = layoutbox.get_renderer(fig)
    do_constrained_layout(fig, renderer, h_pad, w_pad, hspace, wspace)