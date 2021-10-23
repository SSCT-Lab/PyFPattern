def test_rename_model(self):
    'Tests autodetection of renamed models.'
    before = self.make_project_state([self.author_with_book, self.book])
    after = self.make_project_state([self.author_renamed_with_book, self.book_with_author_renamed])
    autodetector = MigrationAutodetector(before, after, MigrationQuestioner({
        'ask_rename_model': True,
    }))
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RenameModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, old_name='Author', new_name='Writer')
    self.assertNumberMigrations(changes, 'otherapp', 0)