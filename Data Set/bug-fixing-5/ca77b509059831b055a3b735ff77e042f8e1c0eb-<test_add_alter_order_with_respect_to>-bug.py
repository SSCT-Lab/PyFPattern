def test_add_alter_order_with_respect_to(self):
    '\n        Tests that setting order_with_respect_to when adding the FK too does\n        things in the right order.\n        '
    before = self.make_project_state([self.author_name])
    after = self.make_project_state([self.book, self.author_with_book_order_wrt])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AddField', 'AlterOrderWithRespectTo'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, model_name='author', name='book')
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='author', order_with_respect_to='book')