def test_poly(self):
    shp_file = os.path.join(TEST_DATA, 'test_poly', 'test_poly.shp')
    model_def = ogrinspect(shp_file, 'MyModel')
    expected = ['# This is an auto-generated Django model module created by ogrinspect.', 'from django.contrib.gis.db import models', '', '', 'class MyModel(models.Model):', '    float = models.FloatField()', '    int = models.{}()'.format(('BigIntegerField' if (GDAL_VERSION >= (2, 0)) else 'FloatField')), '    str = models.CharField(max_length=80)', ('    geom = models.PolygonField(%s)' % self.expected_srid)]
    self.assertEqual(model_def, '\n'.join(expected))