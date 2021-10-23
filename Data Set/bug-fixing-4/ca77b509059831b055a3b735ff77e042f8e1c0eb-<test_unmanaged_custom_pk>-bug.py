def test_unmanaged_custom_pk(self):
    '\n        #23415 - The autodetector must correctly deal with custom FK on\n        unmanaged models.\n        '
    before = self.make_project_state([])
    after = self.make_project_state([self.author_unmanaged_default_pk, self.book])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertEqual(changes['otherapp'][0].operations[0].fields[2][1].remote_field.field_name, 'id')
    before = self.make_project_state([])
    after = self.make_project_state([self.author_unmanaged_custom_pk, self.book])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertEqual(changes['otherapp'][0].operations[0].fields[2][1].remote_field.field_name, 'pk_field')