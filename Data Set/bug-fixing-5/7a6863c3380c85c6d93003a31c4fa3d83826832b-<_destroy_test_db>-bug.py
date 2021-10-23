def _destroy_test_db(self, test_database_name, verbosity):
    '\n        Internal implementation - remove the test db tables.\n        '
    with self.connection._nodb_connection.cursor() as cursor:
        time.sleep(1)
        cursor.execute(('DROP DATABASE %s' % self.connection.ops.quote_name(test_database_name)))