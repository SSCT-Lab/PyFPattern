def test_old_model(self):
    'Tests deletion of old models.'
    before = self.make_project_state([self.author_empty])
    after = self.make_project_state([])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['DeleteModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='Author')