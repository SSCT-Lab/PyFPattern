def test_date_field(self):
    shp_file = os.path.join(TEST_DATA, 'cities', 'cities.shp')
    model_def = ogrinspect(shp_file, 'City')
    expected = ['# This is an auto-generated Django model module created by ogrinspect.', 'from django.contrib.gis.db import models', '', '', 'class City(models.Model):', '    name = models.CharField(max_length=80)', '    population = models.{}()'.format(('BigIntegerField' if (GDAL_VERSION >= (2, 0)) else 'FloatField')), '    density = models.FloatField()', '    created = models.DateField()', '    geom = models.PointField(srid=-1)']
    self.assertEqual(model_def, '\n'.join(expected))