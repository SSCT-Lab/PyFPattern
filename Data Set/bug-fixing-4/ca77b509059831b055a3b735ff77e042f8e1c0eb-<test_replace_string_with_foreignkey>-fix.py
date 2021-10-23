def test_replace_string_with_foreignkey(self):
    '\n        #22300 - Adding an FK in the same "spot" as a deleted CharField should\n        work.\n        '
    changes = self.get_changes([self.author_with_publisher_string], [self.author_with_publisher, self.publisher])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel', 'RemoveField', 'AddField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='Publisher')
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='publisher_name')
    self.assertOperationAttributes(changes, 'testapp', 0, 2, name='publisher')