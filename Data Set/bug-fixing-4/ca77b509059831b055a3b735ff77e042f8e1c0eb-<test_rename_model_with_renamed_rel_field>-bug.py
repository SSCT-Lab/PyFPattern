def test_rename_model_with_renamed_rel_field(self):
    '\n        Tests autodetection of renamed models while simultaneously renaming one\n        of the fields that relate to the renamed model.\n        '
    before = self.make_project_state([self.author_with_book, self.book])
    after = self.make_project_state([self.author_renamed_with_book, self.book_with_field_and_author_renamed])
    autodetector = MigrationAutodetector(before, after, MigrationQuestioner({
        'ask_rename': True,
        'ask_rename_model': True,
    }))
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RenameModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, old_name='Author', new_name='Writer')
    self.assertNumberMigrations(changes, 'otherapp', 1)
    self.assertOperationTypes(changes, 'otherapp', 0, ['RenameField'])
    self.assertOperationAttributes(changes, 'otherapp', 0, 0, old_name='author', new_name='writer')