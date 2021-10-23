def test_remove_field(self):
    'Tests autodetection of removed fields.'
    before = self.make_project_state([self.author_name])
    after = self.make_project_state([self.author_empty])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RemoveField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='name')