@skipUnlessDBFeature('supports_isvalid_lookup')
def test_isvalid_lookup(self):
    invalid_geom = fromstr('POLYGON((0 0, 0 1, 1 1, 1 0, 1 1, 1 0, 0 0))')
    State.objects.create(name='invalid', poly=invalid_geom)
    qs = State.objects.all()
    if (oracle or mysql):
        qs = qs.exclude(name='Kansas')
        self.assertEqual(State.objects.filter(name='Kansas', poly__isvalid=False).count(), 1)
    self.assertEqual(qs.filter(poly__isvalid=False).count(), 1)
    self.assertEqual(qs.filter(poly__isvalid=True).count(), (qs.count() - 1))