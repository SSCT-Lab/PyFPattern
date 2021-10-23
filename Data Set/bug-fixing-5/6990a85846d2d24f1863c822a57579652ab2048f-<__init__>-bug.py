def __init__(self, fig, rect=None, *args, azim=(- 60), elev=30, sharez=None, proj_type='persp', **kwargs):
    "\n        Parameters\n        ----------\n        fig : Figure\n            The parent figure.\n        rect : (float, float, float, float)\n            The ``(left, bottom, width, height)`` axes position.\n        azim : float, optional, default: -60\n            Azimuthal viewing angle.\n        elev : float, optional, default: 30\n            Elevation viewing angle.\n        sharez : Axes3D, optional\n            Other axes to share z-limits with.\n        proj_type : {'persp', 'ortho'}\n            The projection type, default 'persp'.\n        **kwargs\n            Other optional keyword arguments:\n\n            %(Axes3D)s\n\n        Notes\n        -----\n        .. versionadded:: 1.2.1\n            The *sharez* parameter.\n        "
    if (rect is None):
        rect = [0.0, 0.0, 1.0, 1.0]
    self._cids = []
    self.initial_azim = azim
    self.initial_elev = elev
    self.set_proj_type(proj_type)
    self.xy_viewLim = Bbox.unit()
    self.zz_viewLim = Bbox.unit()
    self.xy_dataLim = Bbox.unit()
    self.zz_dataLim = Bbox.unit()
    self.view_init(self.initial_elev, self.initial_azim)
    self._ready = 0
    self._sharez = sharez
    if (sharez is not None):
        self._shared_z_axes.join(self, sharez)
        self._adjustable = 'datalim'
    super().__init__(fig, rect, *args, frameon=True, **kwargs)
    super().set_axis_off()
    self.set_axis_on()
    self.M = None
    self.fmt_zdata = None
    if (self.zaxis is not None):
        self._zcid = self.zaxis.callbacks.connect('units finalize', (lambda : self._on_units_changed(scalez=True)))
    else:
        self._zcid = None
    self._ready = 1
    self.mouse_init()
    self.set_top_view()
    self.patch.set_linewidth(0)
    pseudo_bbox = self.transLimits.inverted().transform([(0, 0), (1, 1)])
    (self._pseudo_w, self._pseudo_h) = (pseudo_bbox[1] - pseudo_bbox[0])
    self.figure.add_axes(self)
    for k in self.spines.keys():
        self.spines[k].set_visible(False)