

def _calc_vertices_regions(self):
    '\n        Calculates the Voronoi vertices and regions of the generators stored\n        in self.points. The vertices will be stored in self.vertices and the\n        regions in self.regions.\n\n        This algorithm was discussed at PyData London 2015 by\n        Tyler Reddy, Ross Hemsley and Nikolai Nowaczyk\n        '
    self._tri = scipy.spatial.ConvexHull(self.points)
    tetrahedrons = self._tri.points[self._tri.simplices]
    tetrahedrons = np.insert(tetrahedrons, 3, np.array([self.center]), axis=1)
    circumcenters = calc_circumcenters(tetrahedrons)
    self.vertices = project_to_sphere(circumcenters, self.center, self.radius)
    simplex_indices = np.arange(self._tri.simplices.shape[0])
    tri_indices = np.column_stack([simplex_indices, simplex_indices, simplex_indices]).ravel()
    point_indices = self._tri.simplices.ravel()
    array_associations = np.dstack((point_indices, tri_indices))[0]
    array_associations = array_associations[np.lexsort((array_associations[(..., 1)], array_associations[(..., 0)]))]
    groups = []
    for (k, g) in itertools.groupby(array_associations, (lambda t: t[0])):
        groups.append(list(list(zip(*list(g)))[1]))
    self.regions = groups
