def _get_test_db_name(self):
    test_database_name = self.connection.settings_dict['TEST']['NAME']
    can_share_in_memory_db = self.connection.features.can_share_in_memory_db
    if (test_database_name and (test_database_name != ':memory:')):
        if (('mode=memory' in test_database_name) and (not can_share_in_memory_db)):
            raise ImproperlyConfigured('Using a shared memory database with `mode=memory` in the database name is not supported in your environment, use `:memory:` instead.')
        return test_database_name
    if can_share_in_memory_db:
        return ('file:memorydb_%s?mode=memory&cache=shared' % self.connection.alias)
    return ':memory:'