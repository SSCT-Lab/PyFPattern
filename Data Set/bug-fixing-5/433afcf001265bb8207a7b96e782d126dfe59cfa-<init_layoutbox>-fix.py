def init_layoutbox(self):
    '\n        Initialize the layoutbox for use in constrained_layout.\n        '
    if (self._layoutbox is None):
        self._layoutbox = layoutbox.LayoutBox(parent=None, name='figlb', artist=self)
        self._layoutbox.constrain_geometry(0.0, 0.0, 1.0, 1.0)