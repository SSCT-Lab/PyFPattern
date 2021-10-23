def test_alter_many_to_many(self):
    before = self.make_project_state([self.author_with_m2m, self.publisher])
    after = self.make_project_state([self.author_with_m2m_blank, self.publisher])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='publishers')