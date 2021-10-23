def _raw_ticks(self, vmin, vmax):
    if (self._nbins == 'auto'):
        nbins = max(min(self.axis.get_tick_space(), 9), max(1, (self._min_n_ticks - 1)))
    else:
        nbins = self._nbins
    while True:
        ticks = self._try_raw_ticks(vmin, vmax, nbins)
        nticks = ((ticks <= vmax) & (ticks >= vmin)).sum()
        if (nticks >= self._min_n_ticks):
            break
        nbins += 1
    self._nbins_used = nbins
    return ticks