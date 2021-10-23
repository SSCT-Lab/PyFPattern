def test_proxy_fk_dependency(self):
    'Tests that FK dependencies still work on proxy models.'
    before = self.make_project_state([])
    after = self.make_project_state([self.author_empty, self.author_proxy_third, self.book_proxy_fk])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='Author')
    self.assertMigrationDependencies(changes, 'testapp', 0, [])
    self.assertNumberMigrations(changes, 'otherapp', 1)
    self.assertOperationTypes(changes, 'otherapp', 0, ['CreateModel'])
    self.assertOperationAttributes(changes, 'otherapp', 0, 0, name='Book')
    self.assertMigrationDependencies(changes, 'otherapp', 0, [('thirdapp', 'auto_1')])
    self.assertNumberMigrations(changes, 'thirdapp', 1)
    self.assertOperationTypes(changes, 'thirdapp', 0, ['CreateModel'])
    self.assertOperationAttributes(changes, 'thirdapp', 0, 0, name='AuthorProxy')
    self.assertMigrationDependencies(changes, 'thirdapp', 0, [('testapp', 'auto_1')])