def test_deconstructible_list(self):
    'Nested deconstruction descends into lists.'
    changes = self.get_changes([self.author_name_deconstructible_list_1], [self.author_name_deconstructible_list_2])
    self.assertEqual(changes, {
        
    })
    changes = self.get_changes([self.author_name_deconstructible_list_1], [self.author_name_deconstructible_list_3])
    self.assertEqual(len(changes), 1)