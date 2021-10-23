def test_deconstruct_field_kwarg(self):
    'Field instances are handled correctly by nested deconstruction.'
    before = self.make_project_state([self.author_name_deconstructible_3])
    after = self.make_project_state([self.author_name_deconstructible_4])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertEqual(changes, {
        
    })