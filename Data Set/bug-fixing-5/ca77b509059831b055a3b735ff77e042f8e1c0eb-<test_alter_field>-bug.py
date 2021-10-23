def test_alter_field(self):
    'Tests autodetection of new fields.'
    before = self.make_project_state([self.author_name])
    after = self.make_project_state([self.author_name_longer])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='name', preserve_default=True)