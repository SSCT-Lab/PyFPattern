

@mock.patch('socket.gethostbyname')
def test04_city(self, gethostbyname):
    'GeoIP city querying methods.'
    gethostbyname.return_value = '128.249.1.1'
    g = GeoIP2(country='<foo>')
    for query in (self.fqdn, self.addr):
        self.assertEqual('US', g.country_code(query), ('Failed for func country_code and query %s' % query))
        self.assertEqual('United States', g.country_name(query), ('Failed for func country_name and query %s' % query))
        self.assertEqual({
            'country_code': 'US',
            'country_name': 'United States',
        }, g.country(query))
        d = g.city(query)
        self.assertEqual('NA', d['continent_code'])
        self.assertEqual('North America', d['continent_name'])
        self.assertEqual('US', d['country_code'])
        self.assertEqual('Houston', d['city'])
        self.assertEqual('TX', d['region'])
        self.assertEqual('America/Chicago', d['time_zone'])
        self.assertFalse(d['is_in_european_union'])
        geom = g.geos(query)
        self.assertIsInstance(geom, GEOSGeometry)
        for (e1, e2) in (geom.tuple, g.coords(query), g.lon_lat(query), g.lat_lon(query)):
            self.assertIsInstance(e1, float)
            self.assertIsInstance(e2, float)
