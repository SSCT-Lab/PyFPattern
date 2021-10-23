def test_citext_cache(self):
    get_citext_oids(connection.alias)
    with self.assertNumQueries(0):
        get_citext_oids(connection.alias)