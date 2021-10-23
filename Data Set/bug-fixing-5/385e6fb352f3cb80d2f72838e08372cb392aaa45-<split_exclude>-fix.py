def split_exclude(self, filter_expr, can_reuse, names_with_path):
    "\n        When doing an exclude against any kind of N-to-many relation, we need\n        to use a subquery. This method constructs the nested query, given the\n        original exclude filter (filter_expr) and the portion up to the first\n        N-to-many relation field.\n\n        For example, if the origin filter is ~Q(child__name='foo'), filter_expr\n        is ('child__name', 'foo') and can_reuse is a set of joins usable for\n        filters in the original query.\n\n        We will turn this into equivalent of:\n            WHERE NOT (pk IN (SELECT parent_id FROM thetable\n                              WHERE name = 'foo' AND parent_id IS NOT NULL))\n\n        It might be worth it to consider using WHERE NOT EXISTS as that has\n        saner null handling, and is easier for the backend's optimizer to\n        handle.\n        "
    query = Query(self.model)
    query.add_filter(filter_expr)
    query.clear_ordering(True)
    (trimmed_prefix, contains_louter) = query.trim_start(names_with_path)
    col = query.select[0]
    select_field = col.target
    alias = col.alias
    if self.is_nullable(select_field):
        lookup_class = select_field.get_lookup('isnull')
        lookup = lookup_class(select_field.get_col(alias), False)
        query.where.add(lookup, AND)
    if (alias in can_reuse):
        pk = select_field.model._meta.pk
        query.bump_prefix(self)
        lookup_class = select_field.get_lookup('exact')
        lookup = lookup_class(pk.get_col(query.select[0].alias), pk.get_col(alias))
        query.where.add(lookup, AND)
        query.external_aliases.add(alias)
    (condition, needed_inner) = self.build_filter((('%s__in' % trimmed_prefix), query), current_negated=True, branch_negated=True, can_reuse=can_reuse)
    if contains_louter:
        (or_null_condition, _) = self.build_filter((('%s__isnull' % trimmed_prefix), True), current_negated=True, branch_negated=True, can_reuse=can_reuse)
        condition.add(or_null_condition, OR)
    return (condition, needed_inner)