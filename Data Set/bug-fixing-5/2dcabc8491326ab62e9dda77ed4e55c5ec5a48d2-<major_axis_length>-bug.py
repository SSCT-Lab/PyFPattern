def major_axis_length(self):
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', 'regionprops and image moments')
        l1 = self.inertia_tensor_eigvals[0]
    return (4 * sqrt(l1))