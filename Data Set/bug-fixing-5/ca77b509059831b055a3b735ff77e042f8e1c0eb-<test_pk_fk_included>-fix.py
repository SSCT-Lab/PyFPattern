def test_pk_fk_included(self):
    '\n        Tests that a relation used as the primary key is kept as part of\n        CreateModel.\n        '
    changes = self.get_changes([], [self.aardvark_pk_fk_author, self.author_name])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel', 'CreateModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='Author')
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='Aardvark')