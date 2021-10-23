def test_add_foo_together(self):
    'Tests index/unique_together detection.'
    changes = self.get_changes([self.author_empty, self.book], [self.author_empty, self.book_foo_together])
    self.assertNumberMigrations(changes, 'otherapp', 1)
    self.assertOperationTypes(changes, 'otherapp', 0, ['AlterUniqueTogether', 'AlterIndexTogether'])
    self.assertOperationAttributes(changes, 'otherapp', 0, 0, name='book', unique_together={('author', 'title')})
    self.assertOperationAttributes(changes, 'otherapp', 0, 1, name='book', index_together={('author', 'title')})