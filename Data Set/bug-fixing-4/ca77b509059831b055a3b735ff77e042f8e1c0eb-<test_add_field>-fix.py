def test_add_field(self):
    'Tests autodetection of new fields.'
    changes = self.get_changes([self.author_empty], [self.author_name])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AddField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='name')