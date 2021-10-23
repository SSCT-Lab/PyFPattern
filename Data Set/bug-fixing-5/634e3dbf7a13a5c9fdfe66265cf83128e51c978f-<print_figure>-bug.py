def print_figure(self, filename, dpi=None, facecolor=None, edgecolor=None, orientation='portrait', format=None, *, bbox_inches=None, **kwargs):
    "\n        Render the figure to hardcopy. Set the figure patch face and edge\n        colors.  This is useful because some of the GUIs have a gray figure\n        face color background and you'll probably want to override this on\n        hardcopy.\n\n        Parameters\n        ----------\n        filename\n            can also be a file object on image backends\n\n        orientation : {'landscape', 'portrait'}, optional\n            only currently applies to PostScript printing.\n\n        dpi : scalar, optional\n            the dots per inch to save the figure in; if None, use savefig.dpi\n\n        facecolor : color spec or None, optional\n            the facecolor of the figure; if None, defaults to savefig.facecolor\n\n        edgecolor : color spec or None, optional\n            the edgecolor of the figure; if None, defaults to savefig.edgecolor\n\n        format : str, optional\n            when set, forcibly set the file format to save to\n\n        bbox_inches : str or `~matplotlib.transforms.Bbox`, optional\n            Bbox in inches. Only the given portion of the figure is\n            saved. If 'tight', try to figure out the tight bbox of\n            the figure. If None, use savefig.bbox\n\n        pad_inches : scalar, optional\n            Amount of padding around the figure when bbox_inches is\n            'tight'. If None, use savefig.pad_inches\n\n        bbox_extra_artists : list of `~matplotlib.artist.Artist`, optional\n            A list of extra artists that will be considered when the\n            tight bbox is calculated.\n\n        "
    if (format is None):
        if isinstance(filename, os.PathLike):
            filename = os.fspath(filename)
        if isinstance(filename, str):
            format = os.path.splitext(filename)[1][1:]
        if ((format is None) or (format == '')):
            format = self.get_default_filetype()
            if isinstance(filename, str):
                filename = ((filename.rstrip('.') + '.') + format)
    format = format.lower()
    canvas = self._get_output_canvas(format)
    print_method = getattr(canvas, ('print_%s' % format))
    if (dpi is None):
        dpi = rcParams['savefig.dpi']
    if (dpi == 'figure'):
        dpi = getattr(self.figure, '_original_dpi', self.figure.dpi)
    with cbook._setattr_cm(self, _is_saving=True, manager=None), cbook._setattr_cm(self.figure, dpi=dpi):
        if (facecolor is None):
            facecolor = rcParams['savefig.facecolor']
        if (edgecolor is None):
            edgecolor = rcParams['savefig.edgecolor']
        origfacecolor = self.figure.get_facecolor()
        origedgecolor = self.figure.get_edgecolor()
        self.figure.set_facecolor(facecolor)
        self.figure.set_edgecolor(edgecolor)
        if (bbox_inches is None):
            bbox_inches = rcParams['savefig.bbox']
        if bbox_inches:
            if (bbox_inches == 'tight'):
                result = print_method(io.BytesIO(), dpi=dpi, facecolor=facecolor, edgecolor=edgecolor, orientation=orientation, dryrun=True, **kwargs)
                renderer = self.figure._cachedRenderer
                bbox_artists = kwargs.pop('bbox_extra_artists', None)
                bbox_inches = self.figure.get_tightbbox(renderer, bbox_extra_artists=bbox_artists)
                pad = kwargs.pop('pad_inches', None)
                if (pad is None):
                    pad = rcParams['savefig.pad_inches']
                bbox_inches = bbox_inches.padded(pad)
            restore_bbox = tight_bbox.adjust_bbox(self.figure, bbox_inches, canvas.fixed_dpi)
            _bbox_inches_restore = (bbox_inches, restore_bbox)
        else:
            _bbox_inches_restore = None
        try:
            result = print_method(filename, dpi=dpi, facecolor=facecolor, edgecolor=edgecolor, orientation=orientation, bbox_inches_restore=_bbox_inches_restore, **kwargs)
        finally:
            if (bbox_inches and restore_bbox):
                restore_bbox()
            self.figure.set_facecolor(origfacecolor)
            self.figure.set_edgecolor(origedgecolor)
            self.figure.set_canvas(self)
        return result