def test_hstore_cache(self):
    with self.assertNumQueries(0):
        get_hstore_oids(connection.alias)