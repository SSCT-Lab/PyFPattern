

def test_reverse_one_to_one_then_m2m(self):
    '\n        A m2m relation can be followed afterr going through the select_related\n        reverse of an o2o.\n        '
    qs = Author.objects.prefetch_related('bio__books').select_related('bio')
    with self.assertNumQueries(1):
        list(qs.all())
    Bio.objects.create(author=self.author1)
    with self.assertNumQueries(2):
        list(qs.all())
