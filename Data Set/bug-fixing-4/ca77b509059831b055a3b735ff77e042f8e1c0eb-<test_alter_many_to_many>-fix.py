def test_alter_many_to_many(self):
    changes = self.get_changes([self.author_with_m2m, self.publisher], [self.author_with_m2m_blank, self.publisher])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='publishers')