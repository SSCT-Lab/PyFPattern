def test_hstore_cache(self):
    get_hstore_oids(connection.alias)
    with self.assertNumQueries(0):
        get_hstore_oids(connection.alias)