def get_sequences(self, cursor, table_name, table_fields=()):
    cursor.execute("\n            SELECT s.relname as sequence_name, col.attname\n            FROM pg_class s\n                JOIN pg_namespace sn ON sn.oid = s.relnamespace\n                JOIN pg_depend d ON d.refobjid = s.oid AND d.refclassid = 'pg_class'::regclass\n                JOIN pg_attrdef ad ON ad.oid = d.objid AND d.classid = 'pg_attrdef'::regclass\n                JOIN pg_attribute col ON col.attrelid = ad.adrelid AND col.attnum = ad.adnum\n                JOIN pg_class tbl ON tbl.oid = ad.adrelid\n                JOIN pg_namespace n ON n.oid = tbl.relnamespace\n            WHERE s.relkind = 'S'\n              AND d.deptype in ('a', 'n')\n              AND n.nspname = 'public'\n              AND tbl.relname = %s\n        ", [table_name])
    return [{
        'name': row[0],
        'table': table_name,
        'column': row[1],
    } for row in cursor.fetchall()]