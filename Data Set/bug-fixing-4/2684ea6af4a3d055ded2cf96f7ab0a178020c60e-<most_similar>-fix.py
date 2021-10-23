def most_similar(self, vector, num_neighbors):
    'Find the approximate `num_neighbors` most similar items.\n\n        Parameters\n        ----------\n        vector : numpy.array\n            Vector for word/document.\n        num_neighbors : int\n            Number of most similar items\n\n        Returns\n        -------\n        list of (str, float)\n            List of most similar items in format [(`item`, `cosine_distance`), ... ]\n\n        '
    (ids, distances) = self.index.get_nns_by_vector(vector, num_neighbors, include_distances=True)
    return [(self.labels[ids[i]], (1 - (distances[i] / 2))) for i in range(len(ids))]