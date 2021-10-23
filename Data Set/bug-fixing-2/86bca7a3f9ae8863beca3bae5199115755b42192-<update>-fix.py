

def update(self, kwargs):
    '\n        Update properties from a dictionary.\n        '
    sentinel = object()
    bbox = kwargs.pop('bbox', sentinel)
    super(Text, self).update(kwargs)
    if (bbox is not sentinel):
        self.set_bbox(bbox)
