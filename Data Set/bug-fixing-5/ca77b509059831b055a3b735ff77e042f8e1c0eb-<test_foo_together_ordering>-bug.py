def test_foo_together_ordering(self):
    '\n        Tests that index/unique_together also triggers on ordering changes.\n        '
    before = self.make_project_state([self.author_empty, self.book_foo_together])
    after = self.make_project_state([self.author_empty, self.book_foo_together_2])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'otherapp', 1)
    self.assertOperationTypes(changes, 'otherapp', 0, ['AlterUniqueTogether', 'AlterIndexTogether'])
    self.assertOperationAttributes(changes, 'otherapp', 0, 0, name='book', unique_together={('title', 'author')})
    self.assertOperationAttributes(changes, 'otherapp', 0, 1, name='book', index_together={('title', 'author')})