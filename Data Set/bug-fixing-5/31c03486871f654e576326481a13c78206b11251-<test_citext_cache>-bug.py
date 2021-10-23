def test_citext_cache(self):
    with self.assertNumQueries(0):
        get_citext_oids(connection.alias)