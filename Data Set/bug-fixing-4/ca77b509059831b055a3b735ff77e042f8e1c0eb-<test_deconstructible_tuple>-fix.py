def test_deconstructible_tuple(self):
    'Nested deconstruction descends into tuples.'
    changes = self.get_changes([self.author_name_deconstructible_tuple_1], [self.author_name_deconstructible_tuple_2])
    self.assertEqual(changes, {
        
    })
    changes = self.get_changes([self.author_name_deconstructible_tuple_1], [self.author_name_deconstructible_tuple_3])
    self.assertEqual(len(changes), 1)