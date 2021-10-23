def test_many_to_many_removed_before_through_model_2(self):
    '\n        Removing a model that contains a ManyToManyField and the "through" model\n        in the same change must remove the field before the model to maintain\n        consistency.\n        '
    changes = self.get_changes([self.book_with_multiple_authors_through_attribution, self.author_name, self.attribution], [self.author_name])
    self.assertNumberMigrations(changes, 'otherapp', 1)
    self.assertOperationTypes(changes, 'otherapp', 0, ['RemoveField', 'RemoveField', 'RemoveField', 'DeleteModel', 'DeleteModel'])
    self.assertOperationAttributes(changes, 'otherapp', 0, 0, name='author', model_name='attribution')
    self.assertOperationAttributes(changes, 'otherapp', 0, 1, name='book', model_name='attribution')
    self.assertOperationAttributes(changes, 'otherapp', 0, 2, name='authors', model_name='book')
    self.assertOperationAttributes(changes, 'otherapp', 0, 3, name='Attribution')
    self.assertOperationAttributes(changes, 'otherapp', 0, 4, name='Book')