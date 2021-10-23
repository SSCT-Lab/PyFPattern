def test_add_alter_order_with_respect_to(self):
    '\n        Tests that setting order_with_respect_to when adding the FK too does\n        things in the right order.\n        '
    changes = self.get_changes([self.author_name], [self.book, self.author_with_book_order_wrt])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AddField', 'AlterOrderWithRespectTo'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, model_name='author', name='book')
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='author', order_with_respect_to='book')