def test_substr_with_expressions(self):
    Author.objects.create(name='John Smith', alias='smithj')
    Author.objects.create(name='Rhonda')
    substr = Substr(Upper('name'), StrIndex('name', V('h')), 5, output_field=CharField())
    authors = Author.objects.annotate(name_part=substr)
    self.assertQuerysetEqual(authors.order_by('name'), ['HN SM', 'HONDA'], (lambda a: a.name_part))