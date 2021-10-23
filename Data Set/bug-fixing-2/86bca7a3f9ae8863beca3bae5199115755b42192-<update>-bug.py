

def update(self, kwargs):
    '\n        Update properties from a dictionary.\n        '
    bbox = kwargs.pop('bbox', None)
    super(Text, self).update(kwargs)
    if bbox:
        self.set_bbox(bbox)
