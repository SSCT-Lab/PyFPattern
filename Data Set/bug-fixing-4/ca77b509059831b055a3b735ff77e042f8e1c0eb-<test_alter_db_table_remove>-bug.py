def test_alter_db_table_remove(self):
    "Tests detection for removing db_table in model's options."
    before = self.make_project_state([self.author_with_db_table_options])
    after = self.make_project_state([self.author_empty])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterModelTable'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='author', table=None)