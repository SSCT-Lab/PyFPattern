def test_substr_with_expressions(self):
    Author.objects.create(name='John Smith', alias='smithj')
    Author.objects.create(name='Rhonda')
    authors = Author.objects.annotate(name_part=Substr('name', 5, 3))
    self.assertQuerysetEqual(authors.order_by('name'), [' Sm', 'da'], (lambda a: a.name_part))