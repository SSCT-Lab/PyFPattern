def test_mapping_option(self):
    expected = "    geom = models.PointField(srid=-1)\n\n\n# Auto-generated `LayerMapping` dictionary for City model\ncity_mapping = {\n    'name': 'Name',\n    'population': 'Population',\n    'density': 'Density',\n    'created': 'Created',\n    'geom': 'POINT',\n}\n"
    shp_file = os.path.join(TEST_DATA, 'cities', 'cities.shp')
    out = StringIO()
    call_command('ogrinspect', shp_file, '--mapping', 'City', stdout=out)
    self.assertIn(expected, out.getvalue())