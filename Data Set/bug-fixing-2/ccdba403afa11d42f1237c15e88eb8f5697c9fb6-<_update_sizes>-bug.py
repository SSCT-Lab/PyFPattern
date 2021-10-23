

def _update_sizes(self, changed):
    horizontal = (self.orientation == 'horizontal')
    (padding_left, padding_top, padding_right, padding_bottom) = self.padding
    padding_x = (padding_left + padding_right)
    padding_y = (padding_top + padding_bottom)
    selfw = self.width
    selfh = self.height
    layout_w = max(0, (selfw - padding_x))
    layout_h = max(0, (selfh - padding_y))
    cx = (self.x + padding_left)
    cy = (self.y + padding_bottom)
    view_opts = self.view_opts
    remove_view = self.remove_view
    for (index, widget, (w, h), (wn, hn), (shw, shh), (shnw, shnh), (shw_min, shh_min), (shwn_min, shhn_min), (shw_max, shh_max), (shwn_max, shhn_max), ph, phn) in changed:
        if ((horizontal and ((shw != shnw) or (w != wn) or (shw_min != shwn_min) or (shw_max != shwn_max))) or ((not horizontal) and ((shh != shnh) or (h != hn) or (shh_min != shhn_min) or (shh_max != shhn_max)))):
            return True
        remove_view(widget, index)
        opt = view_opts[index]
        if horizontal:
            (wo, ho) = opt['size']
            if (shnh is not None):
                (_, h) = opt['size'] = [wo, (shnh * layout_h)]
            else:
                h = ho
            (xo, yo) = opt['pos']
            for (key, value) in phn.items():
                posy = (value * layout_h)
                if (key == 'y'):
                    yo = (posy + cy)
                elif (key == 'top'):
                    yo = (posy - h)
                elif (key == 'center_y'):
                    yo = (posy - (h / 2.0))
            opt['pos'] = [xo, yo]
        else:
            (wo, ho) = opt['size']
            if (shnw is not None):
                (w, _) = opt['size'] = [(shnw * layout_w), ho]
            else:
                w = wo
            (xo, yo) = opt['pos']
            for (key, value) in phn.items():
                posx = (value * layout_w)
                if (key == 'x'):
                    xo = (posx + cx)
                elif (key == 'right'):
                    xo = (posx - w)
                elif (key == 'center_x'):
                    xo = (posx - (w / 2.0))
            opt['pos'] = [xo, yo]
    return relayout
