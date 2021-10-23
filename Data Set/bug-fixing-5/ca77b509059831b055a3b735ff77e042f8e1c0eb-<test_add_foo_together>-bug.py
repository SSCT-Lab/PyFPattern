def test_add_foo_together(self):
    'Tests index/unique_together detection.'
    before = self.make_project_state([self.author_empty, self.book])
    after = self.make_project_state([self.author_empty, self.book_foo_together])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'otherapp', 1)
    self.assertOperationTypes(changes, 'otherapp', 0, ['AlterUniqueTogether', 'AlterIndexTogether'])
    self.assertOperationAttributes(changes, 'otherapp', 0, 0, name='book', unique_together={('author', 'title')})
    self.assertOperationAttributes(changes, 'otherapp', 0, 1, name='book', index_together={('author', 'title')})