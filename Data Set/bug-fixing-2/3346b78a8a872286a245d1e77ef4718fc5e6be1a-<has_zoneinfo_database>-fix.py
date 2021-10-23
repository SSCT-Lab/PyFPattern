

@cached_property
def has_zoneinfo_database(self):
    with self.connection.cursor() as cursor:
        cursor.execute("SELECT CONVERT_TZ('2001-01-01 01:00:00', 'UTC', 'UTC')")
        return (cursor.fetchone()[0] is not None)
