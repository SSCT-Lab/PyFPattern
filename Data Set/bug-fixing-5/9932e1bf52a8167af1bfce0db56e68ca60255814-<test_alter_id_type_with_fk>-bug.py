@override_settings(INSTALLED_APPS=['migrations.migrations_test_apps.alter_fk.author_app', 'migrations.migrations_test_apps.alter_fk.book_app'])
def test_alter_id_type_with_fk(self):
    try:
        executor = MigrationExecutor(connection)
        self.assertTableNotExists('author_app_author')
        self.assertTableNotExists('book_app_book')
        executor.migrate([('author_app', '0001_initial'), ('book_app', '0001_initial')])
        self.assertTableExists('author_app_author')
        self.assertTableExists('book_app_book')
        executor.loader.build_graph()
        executor.migrate([('author_app', '0002_alter_id')])
        executor.loader.build_graph()
    finally:
        with connection.schema_editor() as editor:
            editor.execute((editor.sql_delete_table % {
                'table': 'book_app_book',
            }))
            editor.execute((editor.sql_delete_table % {
                'table': 'author_app_author',
            }))
        self.assertTableNotExists('author_app_author')
        self.assertTableNotExists('book_app_book')