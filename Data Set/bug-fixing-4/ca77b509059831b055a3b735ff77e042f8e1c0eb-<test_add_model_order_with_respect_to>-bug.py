def test_add_model_order_with_respect_to(self):
    '\n        Tests that setting order_with_respect_to when adding the whole model\n        does things in the right order.\n        '
    before = self.make_project_state([])
    after = self.make_project_state([self.book, self.author_with_book_order_wrt])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel', 'AlterOrderWithRespectTo'])
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='author', order_with_respect_to='book')
    self.assertNotIn('_order', [name for (name, field) in changes['testapp'][0].operations[0].fields])