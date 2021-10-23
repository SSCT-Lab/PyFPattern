def _check_satisfy_constraints(self, label, xmin, ymin, xmax, ymax, width, height):
    'Check if constrains are satisfied'
    if (((xmax - xmin) * (ymax - ymin)) < 2):
        return False
    x1 = (float(xmin) / width)
    y1 = (float(ymin) / height)
    x2 = (float(xmax) / width)
    y2 = (float(ymax) / height)
    object_areas = self._calculate_areas(label[:, 1:])
    valid_objects = np.where((((object_areas * width) * height) > 2))[0]
    if (valid_objects.size < 1):
        return False
    intersects = self._intersect(label[valid_objects, 1:], x1, y1, x2, y2)
    coverages = (self._calculate_areas(intersects) / object_areas)
    coverages = coverages[np.where((coverages > 0))[0]]
    if ((coverages.size > 0) and (np.amin(coverages) > self.min_object_covered)):
        return True