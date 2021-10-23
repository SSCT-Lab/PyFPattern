def test_non_circular_foreignkey_dependency_removal(self):
    '\n        If two models with a ForeignKey from one to the other are removed at the\n        same time, the autodetector should remove them in the correct order.\n        '
    changes = self.get_changes([self.author_with_publisher, self.publisher_with_author], [])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RemoveField', 'RemoveField', 'DeleteModel', 'DeleteModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='publisher', model_name='author')
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='author', model_name='publisher')
    self.assertOperationAttributes(changes, 'testapp', 0, 2, name='Author')
    self.assertOperationAttributes(changes, 'testapp', 0, 3, name='Publisher')