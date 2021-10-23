def test_many_to_many_removed_before_through_model(self):
    '\n        Removing a ManyToManyField and the "through" model in the same change\n        must remove the field before the model to maintain consistency.\n        '
    before = self.make_project_state([self.book_with_multiple_authors_through_attribution, self.author_name, self.attribution])
    after = self.make_project_state([self.book_with_no_author, self.author_name])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'otherapp', 1)
    self.assertOperationTypes(changes, 'otherapp', 0, ['RemoveField', 'RemoveField', 'RemoveField', 'DeleteModel'])
    self.assertOperationAttributes(changes, 'otherapp', 0, 0, name='author', model_name='attribution')
    self.assertOperationAttributes(changes, 'otherapp', 0, 1, name='book', model_name='attribution')
    self.assertOperationAttributes(changes, 'otherapp', 0, 2, name='authors', model_name='book')
    self.assertOperationAttributes(changes, 'otherapp', 0, 3, name='Attribution')