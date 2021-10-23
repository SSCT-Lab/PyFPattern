def test_time_field(self):
    ogr_db = get_ogr_db_string()
    if (not ogr_db):
        self.skipTest('Unable to setup an OGR connection to your database')
    try:
        model_def = ogrinspect(ogr_db, 'Measurement', layer_key=AllOGRFields._meta.db_table, decimal=['f_decimal'])
    except GDALException:
        self.skipTest('Unable to setup an OGR connection to your database')
    self.assertTrue(model_def.startswith('# This is an auto-generated Django model module created by ogrinspect.\nfrom django.contrib.gis.db import models\n\n\nclass Measurement(models.Model):\n'))
    self.assertIn('    f_decimal = models.DecimalField(max_digits=0, decimal_places=0)', model_def)
    self.assertIn('    f_int = models.IntegerField()', model_def)
    self.assertIn('    f_datetime = models.DateTimeField()', model_def)
    self.assertIn('    f_time = models.TimeField()', model_def)
    self.assertIn('    f_float = models.FloatField()', model_def)
    self.assertIn('    f_char = models.CharField(max_length=10)', model_def)
    self.assertIn('    f_date = models.DateField()', model_def)
    self.assertIsNotNone(re.search('    geom = models.PolygonField\\(([^\\)])*\\)', model_def))