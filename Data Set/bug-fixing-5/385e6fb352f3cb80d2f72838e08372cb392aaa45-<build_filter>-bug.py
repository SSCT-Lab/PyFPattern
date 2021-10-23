def build_filter(self, filter_expr, branch_negated=False, current_negated=False, can_reuse=None, allow_joins=True, split_subq=True, reuse_with_filtered_relation=False):
    "\n        Build a WhereNode for a single filter clause but don't add it\n        to this Query. Query.add_q() will then add this filter to the where\n        Node.\n\n        The 'branch_negated' tells us if the current branch contains any\n        negations. This will be used to determine if subqueries are needed.\n\n        The 'current_negated' is used to determine if the current filter is\n        negated or not and this will be used to determine if IS NULL filtering\n        is needed.\n\n        The difference between current_negated and branch_negated is that\n        branch_negated is set on first negation, but current_negated is\n        flipped for each negation.\n\n        Note that add_filter will not do any negating itself, that is done\n        upper in the code by add_q().\n\n        The 'can_reuse' is a set of reusable joins for multijoins.\n\n        If 'reuse_with_filtered_relation' is True, then only joins in can_reuse\n        will be reused.\n\n        The method will create a filter clause that can be added to the current\n        query. However, if the filter isn't added to the query then the caller\n        is responsible for unreffing the joins used.\n        "
    if isinstance(filter_expr, dict):
        raise FieldError('Cannot parse keyword query as dict')
    (arg, value) = filter_expr
    if (not arg):
        raise FieldError(('Cannot parse keyword query %r' % arg))
    (lookups, parts, reffed_expression) = self.solve_lookup_type(arg)
    if (not getattr(reffed_expression, 'filterable', True)):
        raise NotSupportedError((reffed_expression.__class__.__name__ + ' is disallowed in the filter clause.'))
    if ((not allow_joins) and (len(parts) > 1)):
        raise FieldError('Joined field references are not permitted in this query')
    pre_joins = self.alias_refcount.copy()
    value = self.resolve_lookup_value(value, can_reuse, allow_joins)
    used_joins = {k for (k, v) in self.alias_refcount.items() if (v > pre_joins.get(k, 0))}
    clause = self.where_class()
    if reffed_expression:
        condition = self.build_lookup(lookups, reffed_expression, value)
        clause.add(condition, AND)
        return (clause, [])
    opts = self.get_meta()
    alias = self.get_initial_alias()
    allow_many = ((not branch_negated) or (not split_subq))
    try:
        join_info = self.setup_joins(parts, opts, alias, can_reuse=can_reuse, allow_many=allow_many, reuse_with_filtered_relation=reuse_with_filtered_relation)
        if isinstance(value, Iterator):
            value = list(value)
        self.check_related_objects(join_info.final_field, value, join_info.opts)
        self._lookup_joins = join_info.joins
    except MultiJoin as e:
        return self.split_exclude(filter_expr, LOOKUP_SEP.join(parts[:e.level]), can_reuse, e.names_with_path)
    used_joins.update(join_info.joins)
    (targets, alias, join_list) = self.trim_joins(join_info.targets, join_info.joins, join_info.path)
    if (can_reuse is not None):
        can_reuse.update(join_list)
    if join_info.final_field.is_relation:
        num_lookups = len(lookups)
        if (num_lookups > 1):
            raise FieldError('Related Field got invalid lookup: {}'.format(lookups[0]))
        if (len(targets) == 1):
            col = targets[0].get_col(alias, join_info.final_field)
        else:
            col = MultiColSource(alias, targets, join_info.targets, join_info.final_field)
    else:
        col = targets[0].get_col(alias, join_info.final_field)
    condition = self.build_lookup(lookups, col, value)
    lookup_type = condition.lookup_name
    clause.add(condition, AND)
    require_outer = ((lookup_type == 'isnull') and (condition.rhs is True) and (not current_negated))
    if (current_negated and ((lookup_type != 'isnull') or (condition.rhs is False))):
        require_outer = True
        if ((lookup_type != 'isnull') and (self.is_nullable(targets[0]) or (self.alias_map[join_list[(- 1)]].join_type == LOUTER))):
            lookup_class = targets[0].get_lookup('isnull')
            clause.add(lookup_class(targets[0].get_col(alias, join_info.targets[0]), False), AND)
    return (clause, (used_joins if (not require_outer) else ()))