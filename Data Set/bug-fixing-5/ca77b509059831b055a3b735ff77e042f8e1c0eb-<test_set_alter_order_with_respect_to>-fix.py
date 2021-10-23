def test_set_alter_order_with_respect_to(self):
    'Tests that setting order_with_respect_to adds a field.'
    changes = self.get_changes([self.book, self.author_with_book], [self.book, self.author_with_book_order_wrt])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterOrderWithRespectTo'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='author', order_with_respect_to='book')