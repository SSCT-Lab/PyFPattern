def draw(self, renderer=None, inframe=False):
    '\n        Draw the secondary axes.\n\n        Consults the parent axes for its limits and converts them\n        using the converter specified by\n        `~.axes._secondary_axes.set_functions` (or *functions*\n        parameter when axes initialized.)\n\n        '
    self._set_lims()
    self._set_scale()
    super().draw(renderer=renderer, inframe=inframe)