def test_multiple_annotation(self):
    multi_field = MultiFields.objects.create(point=Point(1, 1), city=City.objects.get(name='Houston'), poly=Polygon(((1, 1), (1, 2), (2, 2), (2, 1), (1, 1))))
    qs = City.objects.values('name').annotate(distance=functions.Distance('multifields__point', multi_field.city.point)).annotate(count=Count('multifields'))
    self.assertTrue(qs.first())