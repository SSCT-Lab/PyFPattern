def major_axis_length(self):
    l1 = self.inertia_tensor_eigvals[0]
    return (4 * sqrt(l1))