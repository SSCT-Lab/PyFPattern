def test_alter_db_table_remove(self):
    "Tests detection for removing db_table in model's options."
    changes = self.get_changes([self.author_with_db_table_options], [self.author_empty])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterModelTable'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='author', table=None)