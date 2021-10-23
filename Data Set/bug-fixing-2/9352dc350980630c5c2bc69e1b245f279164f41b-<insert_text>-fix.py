

def insert_text(self, substring, from_undo=False):
    'Insert new text at the current cursor position. Override this\n        function in order to pre-process text for input validation.\n        '
    if (self.readonly or (not substring) or (not self._lines)):
        return
    if isinstance(substring, bytes):
        substring = substring.decode('utf8')
    if self.replace_crlf:
        substring = substring.replace('\r\n', '\n')
    mode = self.input_filter
    if (mode is not None):
        chr = type(substring)
        if (chr is bytes):
            int_pat = self._insert_int_patb
        else:
            int_pat = self._insert_int_patu
        if (mode == 'int'):
            substring = re.sub(int_pat, chr(''), substring)
        elif (mode == 'float'):
            if ('.' in self.text):
                substring = re.sub(int_pat, chr(''), substring)
            else:
                substring = '.'.join([re.sub(int_pat, chr(''), k) for k in substring.split(chr('.'), 1)])
        else:
            substring = mode(substring, from_undo)
        if (not substring):
            return
    self._hide_handles(EventLoop.window)
    if ((not from_undo) and self.multiline and self.auto_indent and (substring == '\n')):
        substring = self._auto_indent(substring)
    (cc, cr) = self.cursor
    sci = self.cursor_index
    ci = sci()
    text = self._lines[cr]
    len_str = len(substring)
    new_text = ((text[:cc] + substring) + text[cc:])
    self._set_line_text(cr, new_text)
    wrap = (self._get_text_width(new_text, self.tab_width, self._label_cached) > ((self.width - self.padding[0]) - self.padding[2]))
    if ((len_str > 1) or (substring == '\n') or wrap):
        (start, finish, lines, lineflags, len_lines) = self._get_line_from_cursor(cr, new_text)
        self._refresh_text_from_property('insert', start, finish, lines, lineflags, len_lines)
    self.cursor = self.get_cursor_from_index((ci + len_str))
    self._set_unredo_insert(ci, (ci + len_str), substring, from_undo)
