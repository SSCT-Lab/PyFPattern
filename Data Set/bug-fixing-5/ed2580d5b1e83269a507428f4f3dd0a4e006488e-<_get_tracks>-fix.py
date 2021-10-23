def _get_tracks(self, query):
    'Returns a list of TrackInfo objects for a Beatport query.\n        '
    bp_tracks = self.client.search(query, release_type='track')
    tracks = [self._get_track_info(x) for x in bp_tracks]
    return tracks