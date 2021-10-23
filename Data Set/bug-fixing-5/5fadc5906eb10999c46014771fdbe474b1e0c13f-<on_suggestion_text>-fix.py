def on_suggestion_text(self, instance, value):
    global MarkupLabel
    if (not MarkupLabel):
        from kivy.core.text.markup import MarkupLabel
    cursor_row = self.cursor_row
    if ((cursor_row >= len(self._lines)) or (self.canvas is None)):
        return
    cursor_pos = self.cursor_pos
    txt = self._lines[cursor_row]
    kw = self._get_line_options()
    rct = self._lines_rects[cursor_row]
    lbl = text = None
    if value:
        lbl = MarkupLabel(text=(txt + '[b]{}[/b]'.format(value)), **kw)
    else:
        lbl = Label(**kw)
        text = txt
    lbl.refresh()
    self._lines_labels[cursor_row] = lbl.texture
    rct.size = lbl.size
    self._update_graphics()