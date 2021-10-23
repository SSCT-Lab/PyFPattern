def skip_default(self, field):
    "\n        MySQL doesn't accept default values for TEXT and BLOB types, and\n        implicitly treats these columns as nullable.\n        "
    db_type = field.db_type(self.connection)
    return ((db_type is not None) and (db_type.lower() in {'tinyblob', 'blob', 'mediumblob', 'longblob', 'tinytext', 'text', 'mediumtext', 'longtext'}))