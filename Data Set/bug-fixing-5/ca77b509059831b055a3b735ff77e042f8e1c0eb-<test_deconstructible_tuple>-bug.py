def test_deconstructible_tuple(self):
    'Nested deconstruction descends into tuples.'
    before = self.make_project_state([self.author_name_deconstructible_tuple_1])
    after = self.make_project_state([self.author_name_deconstructible_tuple_2])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertEqual(changes, {
        
    })
    before = self.make_project_state([self.author_name_deconstructible_tuple_1])
    after = self.make_project_state([self.author_name_deconstructible_tuple_3])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertEqual(len(changes), 1)