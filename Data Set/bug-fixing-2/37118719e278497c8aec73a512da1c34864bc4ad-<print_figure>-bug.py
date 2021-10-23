

def print_figure(self, filename, dpi=None, facecolor='w', edgecolor='w', orientation='portrait', format=None, **kwargs):
    "\n        Render the figure to hardcopy. Set the figure patch face and edge\n        colors.  This is useful because some of the GUIs have a gray figure\n        face color background and you'll probably want to override this on\n        hardcopy.\n\n        Arguments are:\n\n        *filename*\n            can also be a file object on image backends\n\n        *orientation*\n            only currently applies to PostScript printing.\n\n        *dpi*\n            the dots per inch to save the figure in; if None, use savefig.dpi\n\n        *facecolor*\n            the facecolor of the figure\n\n        *edgecolor*\n            the edgecolor of the figure\n\n        *orientation*\n            landscape' | 'portrait' (not supported on all backends)\n\n        *format*\n            when set, forcibly set the file format to save to\n\n        *bbox_inches*\n            Bbox in inches. Only the given portion of the figure is\n            saved. If 'tight', try to figure out the tight bbox of\n            the figure. If None, use savefig.bbox\n\n        *pad_inches*\n            Amount of padding around the figure when bbox_inches is\n            'tight'. If None, use savefig.pad_inches\n\n        *bbox_extra_artists*\n            A list of extra artists that will be considered when the\n            tight bbox is calculated.\n\n        "
    self._is_saving = True
    if (format is None):
        if cbook.is_string_like(filename):
            format = os.path.splitext(filename)[1][1:]
        if ((format is None) or (format == '')):
            format = self.get_default_filetype()
            if cbook.is_string_like(filename):
                filename = ((filename.rstrip('.') + '.') + format)
    format = format.lower()
    canvas = self._get_output_canvas(format)
    print_method = getattr(canvas, ('print_%s' % format))
    if (dpi is None):
        dpi = rcParams['savefig.dpi']
    if (dpi == 'figure'):
        dpi = self.figure.dpi
    origDPI = self.figure.dpi
    origfacecolor = self.figure.get_facecolor()
    origedgecolor = self.figure.get_edgecolor()
    self.figure.dpi = dpi
    self.figure.set_facecolor(facecolor)
    self.figure.set_edgecolor(edgecolor)
    bbox_inches = kwargs.pop('bbox_inches', None)
    if (bbox_inches is None):
        bbox_inches = rcParams['savefig.bbox']
    if bbox_inches:
        if (bbox_inches == 'tight'):
            result = print_method(io.BytesIO(), dpi=dpi, facecolor=facecolor, edgecolor=edgecolor, orientation=orientation, dryrun=True, **kwargs)
            renderer = self.figure._cachedRenderer
            bbox_inches = self.figure.get_tightbbox(renderer)
            bbox_artists = kwargs.pop('bbox_extra_artists', None)
            if (bbox_artists is None):
                bbox_artists = self.figure.get_default_bbox_extra_artists()
            bbox_filtered = []
            for a in bbox_artists:
                bbox = a.get_window_extent(renderer)
                if a.get_clip_on():
                    clip_box = a.get_clip_box()
                    if (clip_box is not None):
                        bbox = Bbox.intersection(bbox, clip_box)
                    clip_path = a.get_clip_path()
                    if ((clip_path is not None) and (bbox is not None)):
                        clip_path = clip_path.get_fully_transformed_path()
                        bbox = Bbox.intersection(bbox, clip_path.get_extents())
                if ((bbox is not None) and ((bbox.width != 0) or (bbox.height != 0))):
                    bbox_filtered.append(bbox)
            if bbox_filtered:
                _bbox = Bbox.union(bbox_filtered)
                trans = Affine2D().scale((1.0 / self.figure.dpi))
                bbox_extra = TransformedBbox(_bbox, trans)
                bbox_inches = Bbox.union([bbox_inches, bbox_extra])
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
        self.figure.dpi = origDPI
        self.figure.set_facecolor(origfacecolor)
        self.figure.set_edgecolor(origedgecolor)
        self.figure.set_canvas(self)
        self._is_saving = False
    return result
