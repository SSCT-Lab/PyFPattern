def test_foreign_key_removed_before_target_model(self):
    '\n        Removing an FK and the model it targets in the same change must remove\n        the FK field before the model to maintain consistency.\n        '
    changes = self.get_changes([self.author_with_publisher, self.publisher], [self.author_name])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RemoveField', 'DeleteModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='publisher')
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='Publisher')