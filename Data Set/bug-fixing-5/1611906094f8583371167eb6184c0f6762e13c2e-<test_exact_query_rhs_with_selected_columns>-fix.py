def test_exact_query_rhs_with_selected_columns(self):
    newest_author = Author.objects.create(name='Author 2')
    authors_max_ids = Author.objects.filter(name='Author 2').values('name').annotate(max_id=Max('id')).values('max_id').order_by()
    authors = Author.objects.filter(id=authors_max_ids[:1])
    self.assertEqual(authors.get(), newest_author)