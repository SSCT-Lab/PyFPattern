def test_create_with_through_model(self):
    '\n        Adding a m2m with a through model and the models that use it should be\n        ordered correctly.\n        '
    before = self.make_project_state([])
    after = self.make_project_state([self.author_with_m2m_through, self.publisher, self.contract])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel', 'CreateModel', 'CreateModel', 'AddField', 'AddField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='Author')
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='Contract')
    self.assertOperationAttributes(changes, 'testapp', 0, 2, name='Publisher')
    self.assertOperationAttributes(changes, 'testapp', 0, 3, model_name='contract', name='publisher')
    self.assertOperationAttributes(changes, 'testapp', 0, 4, model_name='author', name='publishers')