def test_rename_model(self):
    'Tests autodetection of renamed models.'
    changes = self.get_changes([self.author_with_book, self.book], [self.author_renamed_with_book, self.book_with_author_renamed], MigrationQuestioner({
        'ask_rename_model': True,
    }))
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RenameModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, old_name='Author', new_name='Writer')
    self.assertNumberMigrations(changes, 'otherapp', 0)