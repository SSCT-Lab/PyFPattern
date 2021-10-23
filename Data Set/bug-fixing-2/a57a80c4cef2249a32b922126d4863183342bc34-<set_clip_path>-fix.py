

def set_clip_path(self, path, transform=None):
    "\n        Set the artist's clip path, which may be:\n\n        - a :class:`~matplotlib.patches.Patch` (or subclass) instance; or\n        - a :class:`~matplotlib.path.Path` instance, in which case a\n          :class:`~matplotlib.transforms.Transform` instance, which will be\n          applied to the path before using it for clipping, must be provided;\n          or\n        - ``None``, to remove a previously set clipping path.\n\n        For efficiency, if the path happens to be an axis-aligned rectangle,\n        this method will set the clipping box to the corresponding rectangle\n        and set the clipping path to ``None``.\n\n        ACCEPTS: [ (:class:`~matplotlib.path.Path`,\n        :class:`~matplotlib.transforms.Transform`) |\n        :class:`~matplotlib.patches.Patch` | None ]\n        "
    from matplotlib.patches import Patch, Rectangle
    success = False
    if (transform is None):
        if isinstance(path, Rectangle):
            self.clipbox = TransformedBbox(Bbox.unit(), path.get_transform())
            self._clippath = None
            success = True
        elif isinstance(path, Patch):
            self._clippath = TransformedPatchPath(path)
            success = True
        elif isinstance(path, tuple):
            (path, transform) = path
    if (path is None):
        self._clippath = None
        success = True
    elif isinstance(path, Path):
        self._clippath = TransformedPath(path, transform)
        success = True
    elif isinstance(path, TransformedPatchPath):
        self._clippath = path
        success = True
    elif isinstance(path, TransformedPath):
        self._clippath = path
        success = True
    if (not success):
        raise TypeError('Invalid arguments to set_clip_path, of type {} and {}'.format(type(path).__name__, type(transform).__name__))
    self.pchanged()
    self.stale = True
