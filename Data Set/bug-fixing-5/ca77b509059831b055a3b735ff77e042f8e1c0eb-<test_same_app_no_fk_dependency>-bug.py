def test_same_app_no_fk_dependency(self):
    '\n        Tests that a migration with a FK between two models of the same app\n        does not have a dependency to itself.\n        '
    before = self.make_project_state([])
    after = self.make_project_state([self.author_with_publisher, self.publisher])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel', 'CreateModel', 'AddField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='Author')
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='Publisher')
    self.assertOperationAttributes(changes, 'testapp', 0, 2, name='publisher')
    self.assertMigrationDependencies(changes, 'testapp', 0, [])