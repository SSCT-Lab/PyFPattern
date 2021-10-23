def test_pk_fk_included(self):
    '\n        Tests that a relation used as the primary key is kept as part of\n        CreateModel.\n        '
    before = self.make_project_state([])
    after = self.make_project_state([self.aardvark_pk_fk_author, self.author_name])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel', 'CreateModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='Author')
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='Aardvark')