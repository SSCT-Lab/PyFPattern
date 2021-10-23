def test_deconstructible_list(self):
    'Nested deconstruction descends into lists.'
    before = self.make_project_state([self.author_name_deconstructible_list_1])
    after = self.make_project_state([self.author_name_deconstructible_list_2])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertEqual(changes, {
        
    })
    before = self.make_project_state([self.author_name_deconstructible_list_1])
    after = self.make_project_state([self.author_name_deconstructible_list_3])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertEqual(len(changes), 1)