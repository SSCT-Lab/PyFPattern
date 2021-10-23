

@cached_property
def has_zoneinfo_database(self):
    with self.connection.cursor() as cursor:
        cursor.execute('SELECT 1 FROM mysql.time_zone LIMIT 1')
        return (cursor.fetchone() is not None)
