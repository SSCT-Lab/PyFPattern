def test_bases_first(self):
    'Tests that bases of other models come first.'
    before = self.make_project_state([])
    after = self.make_project_state([self.aardvark_based_on_author, self.author_name])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel', 'CreateModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='Author')
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='Aardvark')