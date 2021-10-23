def test_facet_tags(self):
    FANTASY_BOOKS = [1, 2, 3, 4, 5, 6, 7]
    SCIFI_BOOKS = [10]
    for book in models.Book.objects.filter(id__in=(FANTASY_BOOKS + SCIFI_BOOKS)):
        if (book.id in FANTASY_BOOKS):
            book.tags.add('Fantasy')
        if (book.id in SCIFI_BOOKS):
            book.tags.add('Science Fiction')
        self.backend.add(book)
    index = self.backend.get_index_for_model(models.Book)
    if index:
        index.refresh()
    fantasy_tag = Tag.objects.get(name='Fantasy')
    scifi_tag = Tag.objects.get(name='Science Fiction')
    results = self.backend.search(MATCH_ALL, models.Book).facet('tags')
    self.assertEqual(results, OrderedDict([(fantasy_tag.id, 7), (None, 5), (scifi_tag.id, 1)]))