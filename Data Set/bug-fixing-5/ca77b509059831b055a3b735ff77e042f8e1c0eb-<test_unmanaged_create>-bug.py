def test_unmanaged_create(self):
    'Tests that the autodetector correctly deals with managed models.'
    before = self.make_project_state([self.author_empty])
    after = self.make_project_state([self.author_empty, self.author_unmanaged])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='AuthorUnmanaged', options={
        'managed': False,
    })