@property
def focus_distance(self):
    'The focale distance of the ellipse.\n\n        The distance between the center and one focus.\n\n        Returns\n        =======\n\n        focus_distance : number\n\n        See Also\n        ========\n\n        foci\n\n        Examples\n        ========\n\n        >>> from sympy import Point, Ellipse\n        >>> p1 = Point(0, 0)\n        >>> e1 = Ellipse(p1, 3, 1)\n        >>> e1.focus_distance\n        2*sqrt(2)\n\n        '
    return Point.distance(self.center, self.foci[0])