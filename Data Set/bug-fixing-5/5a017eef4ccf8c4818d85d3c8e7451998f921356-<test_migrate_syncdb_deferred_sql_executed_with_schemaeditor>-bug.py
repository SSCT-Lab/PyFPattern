@override_settings(INSTALLED_APPS=['migrations.migrations_test_apps.unmigrated_app_syncdb'])
def test_migrate_syncdb_deferred_sql_executed_with_schemaeditor(self):
    '\n        For an app without migrations, editor.execute() is used for executing\n        the syncdb deferred SQL.\n        '
    stdout = io.StringIO()
    with mock.patch.object(BaseDatabaseSchemaEditor, 'execute') as execute:
        call_command('migrate', run_syncdb=True, verbosity=1, stdout=stdout, no_color=True)
        create_table_count = len([call for call in execute.mock_calls if ('CREATE TABLE' in str(call))])
        self.assertEqual(create_table_count, 2)
        self.assertGreater(len(execute.mock_calls), 2)
    stdout = stdout.getvalue()
    self.assertIn('Synchronize unmigrated apps: unmigrated_app_syncdb', stdout)
    self.assertIn('Creating tables...', stdout)
    self.assertIn('Creating table unmigrated_app_syncdb_classroom', stdout)