def get_valid_flags_by_version(cursor):
    '\n    Some role attributes were introduced after certain versions. We want to\n    compile a list of valid flags against the current Postgres version.\n    '
    current_version = cursor.connection.server_version
    return [flag for (flag, version_introduced) in FLAGS_BY_VERSION.items() if (current_version >= version_introduced)]