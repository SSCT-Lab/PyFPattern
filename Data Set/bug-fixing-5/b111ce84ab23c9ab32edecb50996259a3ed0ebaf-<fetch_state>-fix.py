def fetch_state(project, records):
    start = records[(- 1)].datetime
    end = records[0].datetime
    groups = Group.objects.in_bulk((record.value.event.group_id for record in records))
    return {
        'project': project,
        'groups': groups,
        'rules': Rule.objects.in_bulk(itertools.chain.from_iterable((record.value.rules for record in records))),
        'event_counts': (tsdb.get_sums(tsdb.models.group, groups.keys(), start, end) if groups else {
            
        }),
        'user_counts': (tsdb.get_distinct_counts_totals(tsdb.models.users_affected_by_group, groups.keys(), start, end) if groups else {
            
        }),
    }