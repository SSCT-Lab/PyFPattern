def test_poly_multi(self):
    shp_file = os.path.join(TEST_DATA, 'test_poly', 'test_poly.shp')
    model_def = ogrinspect(shp_file, 'MyModel', multi_geom=True)
    self.assertIn('geom = models.MultiPolygonField(srid=-1)', model_def)
    shp_file = os.path.join(TEST_DATA, 'gas_lines', 'gas_leitung.shp')
    model_def = ogrinspect(shp_file, 'MyModel', multi_geom=True)
    self.assertIn('geom = models.MultiLineStringField(srid=-1)', model_def)