def on_suggestion_text(self, instance, value):
    global MarkupLabel
    if (not MarkupLabel):
        from kivy.core.text.markup import MarkupLabel
    cursor_pos = self.cursor_pos
    txt = self._lines[self.cursor_row]
    cr = self.cursor_row
    kw = self._get_line_options()
    rct = self._lines_rects[cr]
    lbl = text = None
    if value:
        lbl = MarkupLabel(text=(txt + '[b]{}[/b]'.format(value)), **kw)
    else:
        lbl = Label(**kw)
        text = txt
    lbl.refresh()
    self._lines_labels[cr] = lbl.texture
    rct.size = lbl.size
    self._update_graphics()