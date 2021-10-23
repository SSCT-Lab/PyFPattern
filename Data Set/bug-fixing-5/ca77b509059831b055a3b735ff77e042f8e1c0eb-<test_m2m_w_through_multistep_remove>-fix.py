def test_m2m_w_through_multistep_remove(self):
    '\n        A model with a m2m field that specifies a "through" model cannot be\n        removed in the same migration as that through model as the schema will\n        pass through an inconsistent state. The autodetector should produce two\n        migrations to avoid this issue.\n        '
    changes = self.get_changes([self.author_with_m2m_through, self.publisher, self.contract], [self.publisher])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RemoveField', 'RemoveField', 'RemoveField', 'DeleteModel', 'DeleteModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='publishers', model_name='author')
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='author', model_name='contract')
    self.assertOperationAttributes(changes, 'testapp', 0, 2, name='publisher', model_name='contract')
    self.assertOperationAttributes(changes, 'testapp', 0, 3, name='Author')
    self.assertOperationAttributes(changes, 'testapp', 0, 4, name='Contract')