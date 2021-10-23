def test_remove_field(self):
    'Tests autodetection of removed fields.'
    changes = self.get_changes([self.author_name], [self.author_empty])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RemoveField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='name')