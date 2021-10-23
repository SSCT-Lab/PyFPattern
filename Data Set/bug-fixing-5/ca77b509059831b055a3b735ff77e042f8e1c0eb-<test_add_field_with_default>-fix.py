def test_add_field_with_default(self):
    '#22030 - Adding a field with a default should work.'
    changes = self.get_changes([self.author_empty], [self.author_name_default])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AddField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='name')