def test_remove_foo_together(self):
    'Tests index/unique_together detection.'
    changes = self.get_changes([self.author_empty, self.book_foo_together], [self.author_empty, self.book])
    self.assertNumberMigrations(changes, 'otherapp', 1)
    self.assertOperationTypes(changes, 'otherapp', 0, ['AlterUniqueTogether', 'AlterIndexTogether'])
    self.assertOperationAttributes(changes, 'otherapp', 0, 0, name='book', unique_together=set())
    self.assertOperationAttributes(changes, 'otherapp', 0, 1, name='book', index_together=set())