def test_deconstructible_dict(self):
    'Nested deconstruction descends into dict values.'
    changes = self.get_changes([self.author_name_deconstructible_dict_1], [self.author_name_deconstructible_dict_2])
    self.assertEqual(changes, {
        
    })
    changes = self.get_changes([self.author_name_deconstructible_dict_1], [self.author_name_deconstructible_dict_3])
    self.assertEqual(len(changes), 1)