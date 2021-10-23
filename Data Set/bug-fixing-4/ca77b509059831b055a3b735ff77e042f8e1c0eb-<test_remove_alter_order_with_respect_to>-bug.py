def test_remove_alter_order_with_respect_to(self):
    '\n        Tests that removing order_with_respect_to when removing the FK too does\n        things in the right order.\n        '
    before = self.make_project_state([self.book, self.author_with_book_order_wrt])
    after = self.make_project_state([self.author_name])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterOrderWithRespectTo', 'RemoveField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='author', order_with_respect_to=None)
    self.assertOperationAttributes(changes, 'testapp', 0, 1, model_name='author', name='book')