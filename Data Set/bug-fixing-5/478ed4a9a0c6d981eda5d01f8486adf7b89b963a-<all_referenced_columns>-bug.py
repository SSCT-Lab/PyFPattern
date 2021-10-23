def all_referenced_columns(conditions):
    flat_conditions = list(chain(*[([c] if is_condition(c) else c) for c in conditions]))
    return set(list(chain(*[columns_in_expr(c[0]) for c in flat_conditions])))