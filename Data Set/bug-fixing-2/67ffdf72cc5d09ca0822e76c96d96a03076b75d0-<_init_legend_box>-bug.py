

def _init_legend_box(self, handles, labels, markerfirst=True):
    '\n        Initialize the legend_box. The legend_box is an instance of\n        the OffsetBox, which is packed with legend handles and\n        texts. Once packed, their location is calculated during the\n        drawing time.\n        '
    fontsize = self._fontsize
    text_list = []
    handle_list = []
    label_prop = dict(verticalalignment='baseline', horizontalalignment='left', fontproperties=self.prop)
    labelboxes = []
    handleboxes = []
    descent = ((0.35 * self._approx_text_height()) * (self.handleheight - 0.7))
    height = ((self._approx_text_height() * self.handleheight) - descent)
    legend_handler_map = self.get_legend_handler_map()
    for (orig_handle, lab) in zip(handles, labels):
        handler = self.get_legend_handler(legend_handler_map, orig_handle)
        if (handler is None):
            warnings.warn('Legend does not support {!r} instances.\nA proxy artist may be used instead.\nSee: http://matplotlib.org/users/legend_guide.html#using-proxy-artist'.format(orig_handle))
            handle_list.append(None)
        else:
            textbox = TextArea(lab, textprops=label_prop, multilinebaseline=True, minimumdescent=True)
            text_list.append(textbox._text)
            labelboxes.append(textbox)
            handlebox = DrawingArea(width=(self.handlelength * fontsize), height=height, xdescent=0.0, ydescent=descent)
            handleboxes.append(handlebox)
            handle_list.append(handler.legend_artist(self, orig_handle, fontsize, handlebox))
    if handleboxes:
        ncol = min(self._ncol, len(handleboxes))
        (nrows, num_largecol) = divmod(len(handleboxes), ncol)
        num_smallcol = (ncol - num_largecol)
        rows_per_col = (([(nrows + 1)] * num_largecol) + ([nrows] * num_smallcol))
        start_idxs = np.concatenate([[0], np.cumsum(rows_per_col)[:(- 1)]])
        cols = zip(start_idxs, rows_per_col)
    else:
        cols = []
    handle_label = list(zip(handleboxes, labelboxes))
    columnbox = []
    for (i0, di) in cols:
        itemBoxes = [HPacker(pad=0, sep=(self.handletextpad * fontsize), children=([h, t] if markerfirst else [t, h]), align='baseline') for (h, t) in handle_label[i0:(i0 + di)]]
        if markerfirst:
            itemBoxes[(- 1)].get_children()[1].set_minimumdescent(False)
        else:
            itemBoxes[(- 1)].get_children()[0].set_minimumdescent(False)
        alignment = ('baseline' if markerfirst else 'right')
        columnbox.append(VPacker(pad=0, sep=(self.labelspacing * fontsize), align=alignment, children=itemBoxes))
    mode = ('expand' if (self._mode == 'expand') else 'fixed')
    sep = (self.columnspacing * fontsize)
    self._legend_handle_box = HPacker(pad=0, sep=sep, align='baseline', mode=mode, children=columnbox)
    self._legend_title_box = TextArea('')
    self._legend_box = VPacker(pad=(self.borderpad * fontsize), sep=(self.labelspacing * fontsize), align='center', children=[self._legend_title_box, self._legend_handle_box])
    self._legend_box.set_figure(self.figure)
    self._legend_box.set_offset(self._findoffset)
    self.texts = text_list
    self.legendHandles = handle_list
