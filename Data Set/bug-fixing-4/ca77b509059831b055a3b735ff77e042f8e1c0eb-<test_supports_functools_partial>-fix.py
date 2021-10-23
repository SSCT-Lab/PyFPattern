def test_supports_functools_partial(self):

    def _content_file_name(instance, filename, key, **kwargs):
        return '{}/{}'.format(instance, filename)

    def content_file_name(key, **kwargs):
        return functools.partial(_content_file_name, key, **kwargs)
    before = [ModelState('testapp', 'Author', [('id', models.AutoField(primary_key=True)), ('file', models.FileField(max_length=200, upload_to=content_file_name('file')))])]
    after = [ModelState('testapp', 'Author', [('id', models.AutoField(primary_key=True)), ('file', models.FileField(max_length=200, upload_to=content_file_name('file')))])]
    changes = self.get_changes(before, after)
    self.assertNumberMigrations(changes, 'testapp', 0)
    args_changed = [ModelState('testapp', 'Author', [('id', models.AutoField(primary_key=True)), ('file', models.FileField(max_length=200, upload_to=content_file_name('other-file')))])]
    changes = self.get_changes(before, args_changed)
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterField'])
    value = changes['testapp'][0].operations[0].field.upload_to
    self.assertEqual((_content_file_name, ('other-file',), {
        
    }), (value.func, value.args, value.keywords))
    kwargs_changed = [ModelState('testapp', 'Author', [('id', models.AutoField(primary_key=True)), ('file', models.FileField(max_length=200, upload_to=content_file_name('file', spam='eggs')))])]
    changes = self.get_changes(before, kwargs_changed)
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterField'])
    value = changes['testapp'][0].operations[0].field.upload_to
    self.assertEqual((_content_file_name, ('file',), {
        'spam': 'eggs',
    }), (value.func, value.args, value.keywords))