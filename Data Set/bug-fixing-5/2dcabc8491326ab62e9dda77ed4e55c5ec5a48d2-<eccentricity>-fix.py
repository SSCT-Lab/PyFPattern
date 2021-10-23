@only2d
def eccentricity(self):
    (l1, l2) = self.inertia_tensor_eigvals
    if (l1 == 0):
        return 0
    return sqrt((1 - (l2 / l1)))