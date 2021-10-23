def test_foo_together_no_changes(self):
    "\n        Tests that index/unique_together doesn't generate a migration if no\n        changes have been made.\n        "
    changes = self.get_changes([self.author_empty, self.book_foo_together], [self.author_empty, self.book_foo_together])
    self.assertEqual(len(changes), 0)