def test_foo_together_no_changes(self):
    "\n        Tests that index/unique_together doesn't generate a migration if no\n        changes have been made.\n        "
    before = self.make_project_state([self.author_empty, self.book_foo_together])
    after = self.make_project_state([self.author_empty, self.book_foo_together])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertEqual(len(changes), 0)