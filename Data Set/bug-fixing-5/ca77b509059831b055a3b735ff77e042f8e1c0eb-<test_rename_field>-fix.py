def test_rename_field(self):
    'Tests autodetection of renamed fields.'
    changes = self.get_changes([self.author_name], [self.author_name_renamed], MigrationQuestioner({
        'ask_rename': True,
    }))
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RenameField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, old_name='name', new_name='names')