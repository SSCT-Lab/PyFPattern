def bounding_box(points):
    minx = float('infinity')
    miny = float('infinity')
    maxx = float('-infinity')
    maxy = float('-infinity')
    for (px, py) in points:
        if (px < minx):
            minx = px
        if (px > maxx):
            maxx = px
        if (py < miny):
            miny = py
        if (py > maxy):
            maxy = py
    return (minx, miny, (maxx - minx), (maxy - miny))