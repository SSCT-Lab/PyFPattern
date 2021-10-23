def test_nested_deconstructible_objects(self):
    '\n        Nested deconstruction is applied recursively to the args/kwargs of\n        deconstructed objects.\n        '
    changes = self.get_changes([self.author_name_nested_deconstructible_1], [self.author_name_nested_deconstructible_2])
    self.assertEqual(changes, {
        
    })
    changes = self.get_changes([self.author_name_nested_deconstructible_1], [self.author_name_nested_deconstructible_changed_arg])
    self.assertEqual(len(changes), 1)
    changes = self.get_changes([self.author_name_nested_deconstructible_1], [self.author_name_nested_deconstructible_extra_arg])
    self.assertEqual(len(changes), 1)
    changes = self.get_changes([self.author_name_nested_deconstructible_1], [self.author_name_nested_deconstructible_changed_kwarg])
    self.assertEqual(len(changes), 1)
    changes = self.get_changes([self.author_name_nested_deconstructible_1], [self.author_name_nested_deconstructible_extra_kwarg])
    self.assertEqual(len(changes), 1)