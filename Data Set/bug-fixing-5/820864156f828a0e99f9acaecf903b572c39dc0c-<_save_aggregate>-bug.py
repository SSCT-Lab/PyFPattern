def _save_aggregate(self, event, hashes, release, **kwargs):
    project = event.project
    all_hashes = self._find_hashes(project, hashes)
    existing_group_id = None
    for h in all_hashes:
        if (h.group_id is not None):
            existing_group_id = h.group_id
            break
        if (h.group_tombstone_id is not None):
            raise HashDiscarded(('Matches group tombstone %s' % h.group_tombstone_id))
    if (existing_group_id is None):
        kwargs['score'] = ScoreClause.calculate(1, kwargs['last_seen'])
        with transaction.atomic():
            short_id = project.next_short_id()
            (group, group_is_new) = (Group.objects.create(project=project, short_id=short_id, **kwargs), True)
    else:
        group = Group.objects.get(id=existing_group_id)
        group_is_new = False
    relevant_group_hashes = set([instance for instance in all_hashes if (instance.group_id == group.id)])
    is_new = False
    new_hashes = [h for h in all_hashes if (h.group_id is None)]
    if new_hashes:
        GroupHash.objects.filter(id__in=[h.id for h in new_hashes]).exclude(state=GroupHash.State.LOCKED_IN_MIGRATION).update(group=group)
        if (group_is_new and (len(new_hashes) == len(all_hashes))):
            is_new = True
        relevant_group_hashes.update(new_hashes)
    can_sample = (features.has('projects:sample-events', project=project) and should_sample((event.data.get('received') or float(event.datetime.strftime('%s'))), (group.data.get('last_received') or float(group.last_seen.strftime('%s'))), group.times_seen))
    if (not is_new):
        is_regression = self._process_existing_aggregate(group=group, event=event, data=kwargs, release=release)
    else:
        is_regression = False
    if (is_new or is_regression):
        is_sample = False
    else:
        is_sample = can_sample
    if (not is_sample):
        GroupHash.record_last_processed_event_id(project.id, [h.id for h in relevant_group_hashes], event.event_id)
    return (group, is_new, is_regression, is_sample)