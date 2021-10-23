def get_constraints(self, cursor, table_name):
    '\n        Retrieve any constraints or keys (unique, pk, fk, check, index) across\n        one or more columns.\n        '
    constraints = {
        
    }
    name_query = '\n            SELECT kc.`constraint_name`, kc.`column_name`,\n                kc.`referenced_table_name`, kc.`referenced_column_name`\n            FROM information_schema.key_column_usage AS kc\n            WHERE\n                kc.table_schema = DATABASE() AND\n                kc.table_name = %s\n        '
    cursor.execute(name_query, [table_name])
    for (constraint, column, ref_table, ref_column) in cursor.fetchall():
        if (constraint not in constraints):
            constraints[constraint] = {
                'columns': OrderedSet(),
                'primary_key': False,
                'unique': False,
                'index': False,
                'check': False,
                'foreign_key': ((ref_table, ref_column) if ref_column else None),
            }
        constraints[constraint]['columns'].add(column)
    type_query = '\n            SELECT c.constraint_name, c.constraint_type\n            FROM information_schema.table_constraints AS c\n            WHERE\n                c.table_schema = DATABASE() AND\n                c.table_name = %s\n        '
    cursor.execute(type_query, [table_name])
    for (constraint, kind) in cursor.fetchall():
        if (kind.lower() == 'primary key'):
            constraints[constraint]['primary_key'] = True
            constraints[constraint]['unique'] = True
        elif (kind.lower() == 'unique'):
            constraints[constraint]['unique'] = True
    cursor.execute(('SHOW INDEX FROM %s' % self.connection.ops.quote_name(table_name)))
    for (table, non_unique, index, colseq, column, type_) in [(x[:5] + (x[10],)) for x in cursor.fetchall()]:
        if (index not in constraints):
            constraints[index] = {
                'columns': OrderedSet(),
                'primary_key': False,
                'unique': False,
                'check': False,
                'foreign_key': None,
            }
        constraints[index]['index'] = True
        constraints[index]['type'] = (Index.suffix if (type_ == 'BTREE') else type_.lower())
        constraints[index]['columns'].add(column)
    for constraint in constraints.values():
        constraint['columns'] = list(constraint['columns'])
    return constraints