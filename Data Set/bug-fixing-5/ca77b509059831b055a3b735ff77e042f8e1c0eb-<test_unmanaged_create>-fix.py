def test_unmanaged_create(self):
    'Tests that the autodetector correctly deals with managed models.'
    changes = self.get_changes([self.author_empty], [self.author_empty, self.author_unmanaged])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='AuthorUnmanaged', options={
        'managed': False,
    })