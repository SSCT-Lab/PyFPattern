def test_rename_field(self):
    'Tests autodetection of renamed fields.'
    before = self.make_project_state([self.author_name])
    after = self.make_project_state([self.author_name_renamed])
    autodetector = MigrationAutodetector(before, after, MigrationQuestioner({
        'ask_rename': True,
    }))
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RenameField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, old_name='name', new_name='names')