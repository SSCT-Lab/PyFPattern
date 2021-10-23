def get_constraints(self, cursor, table_name):
    '\n        Retrieve any constraints or keys (unique, pk, fk, check, index) across\n        one or more columns. Also retrieve the definition of expression-based\n        indexes.\n        '
    constraints = {
        
    }
    cursor.execute("\n            SELECT\n                c.conname,\n                array(\n                    SELECT attname\n                    FROM unnest(c.conkey) WITH ORDINALITY cols(colid, arridx)\n                    JOIN pg_attribute AS ca ON cols.colid = ca.attnum\n                    WHERE ca.attrelid = c.conrelid\n                    ORDER BY cols.arridx\n                ),\n                c.contype,\n                (SELECT fkc.relname || '.' || fka.attname\n                FROM pg_attribute AS fka\n                JOIN pg_class AS fkc ON fka.attrelid = fkc.oid\n                WHERE fka.attrelid = c.confrelid AND fka.attnum = c.confkey[1]),\n                cl.reloptions\n            FROM pg_constraint AS c\n            JOIN pg_class AS cl ON c.conrelid = cl.oid\n            WHERE cl.relname = %s AND pg_catalog.pg_table_is_visible(cl.oid)\n        ", [table_name])
    for (constraint, columns, kind, used_cols, options) in cursor.fetchall():
        constraints[constraint] = {
            'columns': columns,
            'primary_key': (kind == 'p'),
            'unique': (kind in ['p', 'u']),
            'foreign_key': (tuple(used_cols.split('.', 1)) if (kind == 'f') else None),
            'check': (kind == 'c'),
            'index': False,
            'definition': None,
            'options': options,
        }
    cursor.execute("\n            SELECT\n                indexname, array_agg(attname ORDER BY arridx), indisunique, indisprimary,\n                array_agg(ordering ORDER BY arridx), amname, exprdef, s2.attoptions\n            FROM (\n                SELECT\n                    c2.relname as indexname, idx.*, attr.attname, am.amname,\n                    CASE\n                        WHEN idx.indexprs IS NOT NULL THEN\n                            pg_get_indexdef(idx.indexrelid)\n                    END AS exprdef,\n                    CASE am.amname\n                        WHEN 'btree' THEN\n                            CASE (option & 1)\n                                WHEN 1 THEN 'DESC' ELSE 'ASC'\n                            END\n                    END as ordering,\n                    c2.reloptions as attoptions\n                FROM (\n                    SELECT *\n                    FROM pg_index i, unnest(i.indkey, i.indoption) WITH ORDINALITY koi(key, option, arridx)\n                ) idx\n                LEFT JOIN pg_class c ON idx.indrelid = c.oid\n                LEFT JOIN pg_class c2 ON idx.indexrelid = c2.oid\n                LEFT JOIN pg_am am ON c2.relam = am.oid\n                LEFT JOIN pg_attribute attr ON attr.attrelid = c.oid AND attr.attnum = idx.key\n                WHERE c.relname = %s AND pg_catalog.pg_table_is_visible(c.oid)\n            ) s2\n            GROUP BY indexname, indisunique, indisprimary, amname, exprdef, attoptions;\n        ", [table_name])
    for (index, columns, unique, primary, orders, type_, definition, options) in cursor.fetchall():
        if (index not in constraints):
            basic_index = ((type_ == 'btree') and (not index.endswith('_btree')) and (options is None))
            constraints[index] = {
                'columns': (columns if (columns != [None]) else []),
                'orders': (orders if (orders != [None]) else []),
                'primary_key': primary,
                'unique': unique,
                'foreign_key': None,
                'check': False,
                'index': True,
                'type': (Index.suffix if basic_index else type_),
                'definition': definition,
                'options': options,
            }
    return constraints