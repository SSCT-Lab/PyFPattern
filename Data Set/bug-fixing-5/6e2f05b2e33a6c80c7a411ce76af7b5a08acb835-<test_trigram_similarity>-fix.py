def test_trigram_similarity(self):
    search = 'Bat sat on cat.'
    self.assertQuerysetEqual(self.Model.objects.filter(field__trigram_similar=search).annotate(similarity=TrigramSimilarity('field', search)).order_by('-similarity'), [('Cat sat on mat.', 0.625), ('Dog sat on rug.', 0.333333)], transform=(lambda instance: (instance.field, round(instance.similarity, 6))), ordered=True)