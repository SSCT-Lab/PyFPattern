def minor_axis_length(self):
    l2 = self.inertia_tensor_eigvals[(- 1)]
    return (4 * sqrt(l2))