def minor_axis_length(self):
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', 'regionprops and image moments')
        l2 = self.inertia_tensor_eigvals[(- 1)]
    return (4 * sqrt(l2))