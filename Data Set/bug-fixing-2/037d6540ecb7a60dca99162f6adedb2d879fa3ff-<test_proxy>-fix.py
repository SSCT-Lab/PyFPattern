

def test_proxy(self):
    'Testing Lazy-Geometry support (using the GeometryProxy).'
    pnt = Point(0, 0)
    nullcity = City(name='NullCity', point=pnt)
    nullcity.save()
    for bad in [5, 2.0, LineString((0, 0), (1, 1))]:
        with self.assertRaisesMessage(TypeError, 'Cannot set'):
            nullcity.point = bad
    new = Point(5, 23)
    nullcity.point = new
    self.assertEqual(4326, nullcity.point.srid)
    nullcity.save()
    self.assertEqual(new, City.objects.get(name='NullCity').point)
    nullcity.point.x = 23
    nullcity.point.y = 5
    self.assertNotEqual(Point(23, 5, srid=4326), City.objects.get(name='NullCity').point)
    nullcity.save()
    self.assertEqual(Point(23, 5, srid=4326), City.objects.get(name='NullCity').point)
    nullcity.delete()
    shell = LinearRing((0, 0), (0, 90), (100, 90), (100, 0), (0, 0))
    inner = LinearRing((40, 40), (40, 60), (60, 60), (60, 40), (40, 40))
    ply = Polygon(shell, inner)
    nullstate = State(name='NullState', poly=ply)
    self.assertEqual(4326, nullstate.poly.srid)
    nullstate.save()
    ns = State.objects.get(name='NullState')
    self.assertEqual(ply, ns.poly)
    self.assertIsInstance(ns.poly.ogr, gdal.OGRGeometry)
    self.assertEqual(ns.poly.wkb, ns.poly.ogr.wkb)
    self.assertIsInstance(ns.poly.srs, gdal.SpatialReference)
    self.assertEqual('WGS 84', ns.poly.srs.name)
    new_inner = LinearRing((30, 30), (30, 70), (70, 70), (70, 30), (30, 30))
    ns.poly[1] = new_inner
    ply[1] = new_inner
    self.assertEqual(4326, ns.poly.srid)
    ns.save()
    self.assertEqual(ply, State.objects.get(name='NullState').poly)
    ns.delete()
