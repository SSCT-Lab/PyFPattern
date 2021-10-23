def get_cursor_from_xy(self, x, y):
    'Return the (col, row) of the cursor from an (x, y) position.\n        '
    padding_left = self.padding[0]
    padding_top = self.padding[1]
    l = self._lines
    dy = (self.line_height + self.line_spacing)
    cx = (x - self.x)
    scrl_y = self.scroll_y
    scrl_x = self.scroll_x
    scrl_y = ((scrl_y / dy) if (scrl_y > 0) else 0)
    cy = (((self.top - padding_top) + (scrl_y * dy)) - y)
    cy = int(boundary(round(((cy / dy) - 0.5)), 0, (len(l) - 1)))
    _get_text_width = self._get_text_width
    _tab_width = self.tab_width
    _label_cached = self._label_cached
    xoff = 0
    halign = self.halign
    base_dir = (self.base_direction or self._resolved_base_dir)
    auto_halign_r = ((halign == 'auto') and base_dir and ('rtl' in base_dir))
    if (halign == 'center'):
        viewport_width = ((self.width - padding_left) - self.padding[2])
        xoff = int(((viewport_width - self._get_row_width(cy)) / 2))
    elif ((halign == 'right') or auto_halign_r):
        viewport_width = ((self.width - padding_left) - self.padding[2])
        xoff = (viewport_width - self._get_row_width(cy))
    for i in range(0, len(l[cy])):
        if ((((xoff + _get_text_width(l[cy][:i], _tab_width, _label_cached)) + (_get_text_width(l[cy][i], _tab_width, _label_cached) * 0.6)) + padding_left) > (cx + scrl_x)):
            cx = i
            break
    return (cx, cy)