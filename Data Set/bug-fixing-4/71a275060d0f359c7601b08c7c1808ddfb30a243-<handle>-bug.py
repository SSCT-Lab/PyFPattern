def handle(self, **options):

    def _attach_fks(_events):
        project_ids = set([event.project_id for event in _events])
        projects = {p.id: p for p in Project.objects.filter(id__in=project_ids)}
        group_ids = set([event.group_id for event in _events])
        groups = {g.id: g for g in Group.objects.filter(id__in=group_ids)}
        for event in _events:
            event.project = projects[event.project_id]
            event.group = groups[event.group_id]
    from sentry import eventstream
    from sentry.utils.query import RangeQuerySetWrapper
    from_ts = options['from_ts']
    to_ts = options['to_ts']
    from_id = options['from_id']
    to_id = options['to_id']
    if ((from_ts or to_ts) and (from_id or to_id)):
        raise CommandError('You can either limit by primary key, or by timestamp.')
    elif (from_ts and to_ts):
        events = self.get_events_by_timestamp(from_ts, to_ts)
    elif (from_id and to_id):
        events = self.get_events_by_id(from_id, to_id)
    else:
        raise CommandError('Invalid arguments: either use --from/--to-id, or --from/--to-ts.')
    count = events.count()
    self.stdout.write('Events to process: {}\n'.format(count))
    if (count == 0):
        self.stdout.write('Nothing to do.\n')
        sys.exit(0)
    if (not options['no_input']):
        proceed = raw_input('Do you want to continue? [y/N] ')
        if (proceed.lower() not in ['yes', 'y']):
            raise CommandError('Aborted.')
    for event in RangeQuerySetWrapper(events, callbacks=(_attach_fks,)):
        primary_hash = event.get_primary_hash()
        eventstream.insert(group=event.group, event=event, is_new=False, is_sample=False, is_regression=False, is_new_group_environment=False, primary_hash=primary_hash, skip_consume=True)
    self.stdout.write('Done.\n')