def test_custom_deconstructible(self):
    "\n        Two instances which deconstruct to the same value aren't considered a\n        change.\n        "
    before = self.make_project_state([self.author_name_deconstructible_1])
    after = self.make_project_state([self.author_name_deconstructible_2])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertEqual(len(changes), 0)