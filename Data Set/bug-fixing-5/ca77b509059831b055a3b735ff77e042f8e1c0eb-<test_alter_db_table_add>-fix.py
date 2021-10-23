def test_alter_db_table_add(self):
    "Tests detection for adding db_table in model's options."
    changes = self.get_changes([self.author_empty], [self.author_with_db_table_options])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterModelTable'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='author', table='author_one')