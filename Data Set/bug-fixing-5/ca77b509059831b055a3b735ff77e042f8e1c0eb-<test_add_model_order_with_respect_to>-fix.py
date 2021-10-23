def test_add_model_order_with_respect_to(self):
    '\n        Tests that setting order_with_respect_to when adding the whole model\n        does things in the right order.\n        '
    changes = self.get_changes([], [self.book, self.author_with_book_order_wrt])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel', 'AlterOrderWithRespectTo'])
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='author', order_with_respect_to='book')
    self.assertNotIn('_order', [name for (name, field) in changes['testapp'][0].operations[0].fields])