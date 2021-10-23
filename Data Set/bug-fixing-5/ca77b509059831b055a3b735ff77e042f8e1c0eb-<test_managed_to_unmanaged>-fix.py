def test_managed_to_unmanaged(self):
    changes = self.get_changes([self.author_empty, self.author_unmanaged_managed], [self.author_empty, self.author_unmanaged])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterModelOptions'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='authorunmanaged', options={
        'managed': False,
    })