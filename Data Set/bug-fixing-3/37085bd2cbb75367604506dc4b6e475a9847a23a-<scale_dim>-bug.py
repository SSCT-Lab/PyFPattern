def scale_dim(points, size, oneDratio):
    (bbox_x, bbox_y, bbox_w, bbox_h) = bounding_box(points)
    if ((bbox_h == 0) or (bbox_w == 0)):
        raise MultistrokeError('scale_dim() called with invalid points')
    uniformly = (min((bbox_w / bbox_h), (bbox_h / bbox_w)) <= oneDratio)
    if uniformly:
        qx_size = (size / max(bbox_w, bbox_h))
        qy_size = (size / max(bbox_w, bbox_h))
    else:
        qx_size = (size / bbox_w)
        qy_size = (size / bbox_h)
    newpoints = []
    newpoints_append = newpoints.append
    for p in points:
        qx = (p[0] * qx_size)
        qy = (p[1] * qy_size)
        newpoints_append(Vector(qx, qy))
    return newpoints