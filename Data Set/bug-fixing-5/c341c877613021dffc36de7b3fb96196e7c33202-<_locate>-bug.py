def _locate(self, x, y, w, h, y_equivalent_sizes, x_appended_sizes, figW, figH):
    '\n        Parameters\n        ----------\n        x\n        y\n        w\n        h\n        y_equivalent_sizes\n        x_appended_sizes\n        figW\n        figH\n        '
    equivalent_sizes = y_equivalent_sizes
    appended_sizes = x_appended_sizes
    max_equivalent_size = (figH * h)
    total_appended_size = (figW * w)
    karray = self._determine_karray(equivalent_sizes, appended_sizes, max_equivalent_size, total_appended_size)
    ox = self._calc_offsets(appended_sizes, karray)
    ww = ((ox[(- 1)] - ox[0]) / figW)
    ref_h = equivalent_sizes[0]
    hh = (((karray[0] * ref_h[0]) + ref_h[1]) / figH)
    pb = mtransforms.Bbox.from_bounds(x, y, w, h)
    pb1 = mtransforms.Bbox.from_bounds(x, y, ww, hh)
    pb1_anchored = pb1.anchored(self.get_anchor(), pb)
    (x0, y0) = (pb1_anchored.x0, pb1_anchored.y0)
    return (x0, y0, ox, hh)