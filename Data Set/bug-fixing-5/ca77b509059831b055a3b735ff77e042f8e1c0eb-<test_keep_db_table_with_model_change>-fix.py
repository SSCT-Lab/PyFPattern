def test_keep_db_table_with_model_change(self):
    '\n        Tests when model changes but db_table stays as-is, autodetector must not\n        create more than one operation.\n        '
    changes = self.get_changes([self.author_with_db_table_options], [self.author_renamed_with_db_table_options], MigrationQuestioner({
        'ask_rename_model': True,
    }))
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RenameModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, old_name='Author', new_name='NewAuthor')