def test_swappable_first_inheritance(self):
    'Tests that swappable models get their CreateModel first.'
    before = self.make_project_state([])
    after = self.make_project_state([self.custom_user, self.aardvark])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'thirdapp', 1)
    self.assertOperationTypes(changes, 'thirdapp', 0, ['CreateModel', 'CreateModel'])
    self.assertOperationAttributes(changes, 'thirdapp', 0, 0, name='CustomUser')
    self.assertOperationAttributes(changes, 'thirdapp', 0, 1, name='Aardvark')