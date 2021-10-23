

def rotate(self, angle):
    'Rotate the vector with an angle in degrees.\n\n        >>> v = Vector(100, 0)\n        >>> v.rotate(45)\n        [70.71067811865476, 70.71067811865474]\n\n        '
    angle = math.radians(angle)
    return Vector(((self[0] * math.cos(angle)) - (self[1] * math.sin(angle))), ((self[1] * math.cos(angle)) + (self[0] * math.sin(angle))))
