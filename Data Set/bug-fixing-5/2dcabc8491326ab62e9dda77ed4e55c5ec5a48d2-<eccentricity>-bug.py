@only2d
def eccentricity(self):
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', 'regionprops and image moments')
        (l1, l2) = self.inertia_tensor_eigvals
    if (l1 == 0):
        return 0
    return sqrt((1 - (l2 / l1)))