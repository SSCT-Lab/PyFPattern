def unmerge(self, project_id, new_group_id, event_ids):
    if (not event_ids):
        return
    self._send(project_id, 'unmerge', extra_data=({
        'project_id': project_id,
        'new_group_id': new_group_id,
        'event_ids': event_ids,
        'datetime': datetime.now(tz=pytz.utc),
    },))