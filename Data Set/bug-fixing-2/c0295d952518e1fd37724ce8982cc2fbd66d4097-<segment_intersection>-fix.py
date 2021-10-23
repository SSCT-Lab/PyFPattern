

@staticmethod
def segment_intersection(v1, v2, v3, v4):
    '\n        Finds the intersection point between segments (1)v1->v2 and (2)v3->v4\n        and returns it as a vector object.\n\n        >>> a = (98, 28)\n        >>> b = (72, 33)\n        >>> c = (10, -5)\n        >>> d = (20, 88)\n        >>> Vector.segment_intersection(a, b, c, d)\n        None\n\n        >>> a = (0, 0)\n        >>> b = (10, 10)\n        >>> c = (0, 10)\n        >>> d = (10, 0)\n        >>> Vector.segment_intersection(a, b, c, d)\n        [5, 5]\n        '
    (x1, x2, x3, x4) = (float(v1[0]), float(v2[0]), float(v3[0]), float(v4[0]))
    (y1, y2, y3, y4) = (float(v1[1]), float(v2[1]), float(v3[1]), float(v4[1]))
    u = ((x1 * y2) - (y1 * x2))
    v = ((x3 * y4) - (y3 * x4))
    denom = (((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4)))
    if (denom == 0):
        return None
    px = (((u * (x3 - x4)) - ((x1 - x2) * v)) / denom)
    py = (((u * (y3 - y4)) - ((y1 - y2) * v)) / denom)
    c1 = ((x1 <= px <= x2) or (x2 <= px <= x1) or (x1 == x2))
    c2 = ((y1 <= py <= y2) or (y2 <= py <= y1) or (y1 == y2))
    c3 = ((x3 <= px <= x4) or (x4 <= px <= x3) or (x3 == x4))
    c4 = ((y3 <= py <= y4) or (y4 <= py <= y3) or (y3 == y4))
    if ((c1 and c2) and (c3 and c4)):
        return Vector(px, py)
    else:
        return None
