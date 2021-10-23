def test_old_model(self):
    'Tests deletion of old models.'
    changes = self.get_changes([self.author_empty], [])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['DeleteModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='Author')