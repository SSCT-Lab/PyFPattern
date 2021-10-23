def test_add_field_and_foo_together(self):
    '\n        Tests that added fields will be created before using them in\n        index/unique_together.\n        '
    changes = self.get_changes([self.author_empty, self.book], [self.author_empty, self.book_foo_together_3])
    self.assertNumberMigrations(changes, 'otherapp', 1)
    self.assertOperationTypes(changes, 'otherapp', 0, ['AddField', 'AlterUniqueTogether', 'AlterIndexTogether'])
    self.assertOperationAttributes(changes, 'otherapp', 0, 1, name='book', unique_together={('title', 'newfield')})
    self.assertOperationAttributes(changes, 'otherapp', 0, 2, name='book', index_together={('title', 'newfield')})