def test_proxy_custom_pk(self):
    '\n        #23415 - The autodetector must correctly deal with custom FK on proxy\n        models.\n        '
    before = self.make_project_state([])
    after = self.make_project_state([self.author_empty, self.author_proxy_third, self.book_proxy_fk])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertEqual(changes['otherapp'][0].operations[0].fields[2][1].remote_field.field_name, 'id')
    before = self.make_project_state([])
    after = self.make_project_state([self.author_custom_pk, self.author_proxy_third, self.book_proxy_fk])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertEqual(changes['otherapp'][0].operations[0].fields[2][1].remote_field.field_name, 'pk_field')