def test_fk_dependency_other_app(self):
    "\n        #23100 - Tests that ForeignKeys correctly depend on other apps' models.\n        "
    before = self.make_project_state([self.author_name, self.book])
    after = self.make_project_state([self.author_with_book, self.book])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AddField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='book')
    self.assertMigrationDependencies(changes, 'testapp', 0, [('otherapp', '__first__')])