def test_alter_db_table_change(self):
    "Tests detection for changing db_table in model's options'."
    before = self.make_project_state([self.author_with_db_table_options])
    after = self.make_project_state([self.author_with_new_db_table_options])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterModelTable'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='author', table='author_two')