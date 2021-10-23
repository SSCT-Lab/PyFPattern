def test_alter_db_table_no_changes(self):
    "\n        Tests that alter_db_table doesn't generate a migration if no changes\n        have been made.\n        "
    changes = self.get_changes([self.author_with_db_table_options], [self.author_with_db_table_options])
    self.assertEqual(len(changes), 0)