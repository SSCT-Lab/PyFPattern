def most_similar(self, vector, num_neighbors):
    'Find the top-N most similar items'
    (ids, distances) = self.index.get_nns_by_vector(vector, num_neighbors, include_distances=True)
    return [(self.labels[ids[i]], (1 - (distances[i] / 2))) for i in range(len(ids))]