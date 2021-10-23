

def get_constraints(self, cursor, table_name):
    '\n        Retrieves any constraints or keys (unique, pk, fk, check, index) across one or more columns.\n        '
    constraints = {
        
    }
    cursor.execute("\n            SELECT\n                user_constraints.constraint_name,\n                LOWER(cols.column_name) AS column_name,\n                CASE user_constraints.constraint_type\n                    WHEN 'P' THEN 1\n                    ELSE 0\n                END AS is_primary_key,\n                CASE user_indexes.uniqueness\n                    WHEN 'UNIQUE' THEN 1\n                    ELSE 0\n                END AS is_unique,\n                CASE user_constraints.constraint_type\n                    WHEN 'C' THEN 1\n                    ELSE 0\n                END AS is_check_constraint\n            FROM\n                user_constraints\n            INNER JOIN\n                user_indexes ON user_indexes.index_name = user_constraints.index_name\n            LEFT OUTER JOIN\n                user_cons_columns cols ON user_constraints.constraint_name = cols.constraint_name\n            WHERE\n                (\n                    user_constraints.constraint_type = 'P' OR\n                    user_constraints.constraint_type = 'U'\n                )\n                AND user_constraints.table_name = UPPER(%s)\n            ORDER BY cols.position\n        ", [table_name])
    for (constraint, column, pk, unique, check) in cursor.fetchall():
        if (constraint not in constraints):
            constraints[constraint] = {
                'columns': [],
                'primary_key': pk,
                'unique': unique,
                'foreign_key': None,
                'check': check,
                'index': True,
            }
        constraints[constraint]['columns'].append(column)
    cursor.execute("\n            SELECT\n                cons.constraint_name,\n                LOWER(cols.column_name) AS column_name\n            FROM\n                user_constraints cons\n            LEFT OUTER JOIN\n                user_cons_columns cols ON cons.constraint_name = cols.constraint_name\n            WHERE\n                cons.constraint_type = 'C' AND\n                cons.table_name = UPPER(%s)\n            ORDER BY cols.position\n        ", [table_name])
    for (constraint, column) in cursor.fetchall():
        if (constraint not in constraints):
            constraints[constraint] = {
                'columns': [],
                'primary_key': False,
                'unique': False,
                'foreign_key': None,
                'check': True,
                'index': False,
            }
        constraints[constraint]['columns'].append(column)
    cursor.execute("\n            SELECT\n                cons.constraint_name,\n                LOWER(cols.column_name) AS column_name,\n                LOWER(rcons.table_name),\n                LOWER(rcols.column_name)\n            FROM\n                user_constraints cons\n            INNER JOIN\n                user_constraints rcons ON cons.r_constraint_name = rcons.constraint_name\n            INNER JOIN\n                user_cons_columns rcols ON rcols.constraint_name = rcons.constraint_name\n            LEFT OUTER JOIN\n                user_cons_columns cols ON cons.constraint_name = cols.constraint_name\n            WHERE\n                cons.constraint_type = 'R' AND\n                cons.table_name = UPPER(%s)\n            ORDER BY cols.position\n        ", [table_name])
    for (constraint, column, other_table, other_column) in cursor.fetchall():
        if (constraint not in constraints):
            constraints[constraint] = {
                'columns': [],
                'primary_key': False,
                'unique': False,
                'foreign_key': (other_table, other_column),
                'check': False,
                'index': False,
            }
        constraints[constraint]['columns'].append(column)
    cursor.execute('\n            SELECT\n                cols.index_name, LOWER(cols.column_name), cols.descend,\n                LOWER(ind.index_type)\n            FROM\n                user_ind_columns cols, user_indexes ind\n            WHERE\n                cols.table_name = UPPER(%s) AND\n                NOT EXISTS (\n                    SELECT 1\n                    FROM user_constraints cons\n                    WHERE cols.index_name = cons.index_name\n                ) AND cols.index_name = ind.index_name\n            ORDER BY cols.column_position\n        ', [table_name])
    for (constraint, column, order, type_) in cursor.fetchall():
        if (constraint not in constraints):
            constraints[constraint] = {
                'columns': [],
                'orders': [],
                'primary_key': False,
                'unique': False,
                'foreign_key': None,
                'check': False,
                'index': True,
                'type': ('btree' if (type_ == 'normal') else type_),
            }
        constraints[constraint]['columns'].append(column)
        constraints[constraint]['orders'].append(order)
    return constraints
