def test_many_to_many_changed_to_concrete_field(self):
    '\n        #23938 - Tests that changing a ManyToManyField into a concrete field\n        first removes the m2m field and then adds the concrete field.\n        '
    changes = self.get_changes([self.author_with_m2m, self.publisher], [self.author_with_former_m2m])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RemoveField', 'AddField', 'DeleteModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='publishers', model_name='author')
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='publishers', model_name='author')
    self.assertOperationAttributes(changes, 'testapp', 0, 2, name='Publisher')
    self.assertOperationFieldAttributes(changes, 'testapp', 0, 1, max_length=100)