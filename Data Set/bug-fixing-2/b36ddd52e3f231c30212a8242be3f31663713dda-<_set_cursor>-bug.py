

def _set_cursor(self, pos):
    if (not self._lines):
        self._trigger_refresh_text()
        return
    l = self._lines
    cr = boundary(pos[1], 0, (len(l) - 1))
    cc = boundary(pos[0], 0, len(l[cr]))
    cursor = (cc, cr)
    if (self._cursor == cursor):
        return
    self._cursor = cursor
    padding_left = self.padding[0]
    padding_right = self.padding[2]
    viewport_width = ((self.width - padding_left) - padding_right)
    sx = self.scroll_x
    offset = self.cursor_offset()
    if (offset > (viewport_width + sx)):
        self.scroll_x = (offset - viewport_width)
    if (offset < sx):
        self.scroll_x = offset
    dy = (self.line_height + self.line_spacing)
    offsety = (cr * dy)
    sy = self.scroll_y
    padding_top = self.padding[1]
    padding_bottom = self.padding[3]
    viewport_height = (((self.height - padding_top) - padding_bottom) - dy)
    if (offsety > (viewport_height + sy)):
        sy = (offsety - viewport_height)
    if (offsety < sy):
        sy = offsety
    self.scroll_y = sy
    return True
