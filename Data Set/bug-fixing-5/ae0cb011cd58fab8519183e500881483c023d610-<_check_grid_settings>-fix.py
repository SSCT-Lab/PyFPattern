def _check_grid_settings(self, obj, kinds, kws={
    
}):
    import matplotlib as mpl

    def is_grid_on():
        xticks = self.plt.gca().xaxis.get_major_ticks()
        yticks = self.plt.gca().yaxis.get_major_ticks()
        if self.mpl_ge_3_1_0:
            xoff = all(((not g.gridline.get_visible()) for g in xticks))
            yoff = all(((not g.gridline.get_visible()) for g in yticks))
        else:
            xoff = all(((not g.gridOn) for g in xticks))
            yoff = all(((not g.gridOn) for g in yticks))
        return (not (xoff and yoff))
    spndx = 1
    for kind in kinds:
        self.plt.subplot(1, (4 * len(kinds)), spndx)
        spndx += 1
        mpl.rc('axes', grid=False)
        obj.plot(kind=kind, **kws)
        assert (not is_grid_on())
        self.plt.subplot(1, (4 * len(kinds)), spndx)
        spndx += 1
        mpl.rc('axes', grid=True)
        obj.plot(kind=kind, grid=False, **kws)
        assert (not is_grid_on())
        if (kind != 'pie'):
            self.plt.subplot(1, (4 * len(kinds)), spndx)
            spndx += 1
            mpl.rc('axes', grid=True)
            obj.plot(kind=kind, **kws)
            assert is_grid_on()
            self.plt.subplot(1, (4 * len(kinds)), spndx)
            spndx += 1
            mpl.rc('axes', grid=False)
            obj.plot(kind=kind, grid=True, **kws)
            assert is_grid_on()