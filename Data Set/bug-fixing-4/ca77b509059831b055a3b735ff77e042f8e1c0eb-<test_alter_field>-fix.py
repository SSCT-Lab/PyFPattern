def test_alter_field(self):
    'Tests autodetection of new fields.'
    changes = self.get_changes([self.author_name], [self.author_name_longer])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='name', preserve_default=True)