def test_rename_field_and_foo_together(self):
    '\n        Tests that removed fields will be removed after updating\n        index/unique_together.\n        '
    before = self.make_project_state([self.author_empty, self.book_foo_together_3])
    after = self.make_project_state([self.author_empty, self.book_foo_together_4])
    autodetector = MigrationAutodetector(before, after, MigrationQuestioner({
        'ask_rename': True,
    }))
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'otherapp', 1)
    self.assertOperationTypes(changes, 'otherapp', 0, ['RenameField', 'AlterUniqueTogether', 'AlterIndexTogether'])
    self.assertOperationAttributes(changes, 'otherapp', 0, 1, name='book', unique_together={('title', 'newfield2')})
    self.assertOperationAttributes(changes, 'otherapp', 0, 2, name='book', index_together={('title', 'newfield2')})