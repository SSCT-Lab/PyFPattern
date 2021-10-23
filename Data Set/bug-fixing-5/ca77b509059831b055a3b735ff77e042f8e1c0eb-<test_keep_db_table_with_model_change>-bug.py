def test_keep_db_table_with_model_change(self):
    '\n        Tests when model changes but db_table stays as-is, autodetector must not\n        create more than one operation.\n        '
    before = self.make_project_state([self.author_with_db_table_options])
    after = self.make_project_state([self.author_renamed_with_db_table_options])
    autodetector = MigrationAutodetector(before, after, MigrationQuestioner({
        'ask_rename_model': True,
    }))
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RenameModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, old_name='Author', new_name='NewAuthor')