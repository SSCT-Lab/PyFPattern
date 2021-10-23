def test_deconstructible_dict(self):
    'Nested deconstruction descends into dict values.'
    before = self.make_project_state([self.author_name_deconstructible_dict_1])
    after = self.make_project_state([self.author_name_deconstructible_dict_2])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertEqual(changes, {
        
    })
    before = self.make_project_state([self.author_name_deconstructible_dict_1])
    after = self.make_project_state([self.author_name_deconstructible_dict_3])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertEqual(len(changes), 1)