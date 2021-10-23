def test_add_field_with_default(self):
    '#22030 - Adding a field with a default should work.'
    before = self.make_project_state([self.author_empty])
    after = self.make_project_state([self.author_name_default])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AddField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='name')