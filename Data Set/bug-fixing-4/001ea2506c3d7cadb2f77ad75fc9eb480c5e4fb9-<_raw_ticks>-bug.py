def _raw_ticks(self, vmin, vmax):
    nbins = self._nbins
    if (nbins == 'auto'):
        nbins = max(min(self.axis.get_tick_space(), 9), 1)
    (scale, offset) = scale_range(vmin, vmax, nbins)
    if self._integer:
        scale = max(1, scale)
    vmin = (vmin - offset)
    vmax = (vmax - offset)
    raw_step = ((vmax - vmin) / nbins)
    scaled_raw_step = (raw_step / scale)
    best_vmax = vmax
    best_vmin = vmin
    for step in self._steps:
        if (step < scaled_raw_step):
            continue
        step *= scale
        best_vmin = ((vmin // step) * step)
        best_vmax = (best_vmin + (step * nbins))
        if (best_vmax >= vmax):
            break
    low = round((Base(step).le((vmin - best_vmin)) / step))
    high = round((Base(step).ge((vmax - best_vmin)) / step))
    return (((np.arange(low, (high + 1)) * step) + best_vmin) + offset)