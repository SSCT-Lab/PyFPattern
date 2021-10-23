def test_foo_together_remove_fk(self):
    'Tests unique_together and field removal detection & ordering'
    before = self.make_project_state([self.author_empty, self.book_foo_together])
    after = self.make_project_state([self.author_empty, self.book_with_no_author])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'otherapp', 1)
    self.assertOperationTypes(changes, 'otherapp', 0, ['AlterUniqueTogether', 'AlterIndexTogether', 'RemoveField'])
    self.assertOperationAttributes(changes, 'otherapp', 0, 0, name='book', unique_together=set())
    self.assertOperationAttributes(changes, 'otherapp', 0, 1, name='book', index_together=set())
    self.assertOperationAttributes(changes, 'otherapp', 0, 2, model_name='book', name='author')