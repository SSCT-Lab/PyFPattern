def test_alter_db_table_no_changes(self):
    "\n        Tests that alter_db_table doesn't generate a migration if no changes\n        have been made.\n        "
    before = self.make_project_state([self.author_with_db_table_options])
    after = self.make_project_state([self.author_with_db_table_options])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertEqual(len(changes), 0)