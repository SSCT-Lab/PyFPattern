def test_supports_functools_partial(self):

    def _content_file_name(instance, filename, key, **kwargs):
        return '{}/{}'.format(instance, filename)

    def content_file_name(key, **kwargs):
        return functools.partial(_content_file_name, key, **kwargs)
    before = self.make_project_state([ModelState('testapp', 'Author', [('id', models.AutoField(primary_key=True)), ('file', models.FileField(max_length=200, upload_to=content_file_name('file')))])])
    after = self.make_project_state([ModelState('testapp', 'Author', [('id', models.AutoField(primary_key=True)), ('file', models.FileField(max_length=200, upload_to=content_file_name('file')))])])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 0)
    args_changed = self.make_project_state([ModelState('testapp', 'Author', [('id', models.AutoField(primary_key=True)), ('file', models.FileField(max_length=200, upload_to=content_file_name('other-file')))])])
    autodetector = MigrationAutodetector(before, args_changed)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterField'])
    value = changes['testapp'][0].operations[0].field.upload_to
    self.assertEqual((_content_file_name, ('other-file',), {
        
    }), (value.func, value.args, value.keywords))
    kwargs_changed = self.make_project_state([ModelState('testapp', 'Author', [('id', models.AutoField(primary_key=True)), ('file', models.FileField(max_length=200, upload_to=content_file_name('file', spam='eggs')))])])
    autodetector = MigrationAutodetector(before, kwargs_changed)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterField'])
    value = changes['testapp'][0].operations[0].field.upload_to
    self.assertEqual((_content_file_name, ('file',), {
        'spam': 'eggs',
    }), (value.func, value.args, value.keywords))