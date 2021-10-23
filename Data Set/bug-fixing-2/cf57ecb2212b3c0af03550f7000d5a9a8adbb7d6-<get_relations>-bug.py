

def get_relations(self, cursor, table_name):
    '\n        Return a dictionary of {field_name: (field_name_other_table, other_table)}\n        representing all relationships to the given table.\n        '
    table_name = table_name.upper()
    cursor.execute('\n    SELECT ta.column_name, tb.table_name, tb.column_name\n    FROM   user_constraints, USER_CONS_COLUMNS ca, USER_CONS_COLUMNS cb,\n           user_tab_cols ta, user_tab_cols tb\n    WHERE  user_constraints.table_name = %s AND\n           ta.table_name = user_constraints.table_name AND\n           ta.column_name = ca.column_name AND\n           ca.table_name = ta.table_name AND\n           user_constraints.constraint_name = ca.constraint_name AND\n           user_constraints.r_constraint_name = cb.constraint_name AND\n           cb.table_name = tb.table_name AND\n           cb.column_name = tb.column_name AND\n           ca.position = cb.position', [table_name])
    relations = {
        
    }
    for row in cursor.fetchall():
        relations[row[0].lower()] = (row[2].lower(), row[1].lower())
    return relations
