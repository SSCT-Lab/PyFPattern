def delete_groups(self, project_id, group_ids):
    if (not group_ids):
        return
    self._send(project_id, 'delete_groups', extra_data=({
        'project_id': project_id,
        'group_ids': group_ids,
        'datetime': datetime.now(tz=pytz.utc),
    },), asynchronous=False)