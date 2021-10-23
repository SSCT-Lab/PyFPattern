def test_deconstruct_field_kwarg(self):
    'Field instances are handled correctly by nested deconstruction.'
    changes = self.get_changes([self.author_name_deconstructible_3], [self.author_name_deconstructible_4])
    self.assertEqual(changes, {
        
    })