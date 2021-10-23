def test_custom_deconstructible(self):
    "\n        Two instances which deconstruct to the same value aren't considered a\n        change.\n        "
    changes = self.get_changes([self.author_name_deconstructible_1], [self.author_name_deconstructible_2])
    self.assertEqual(len(changes), 0)