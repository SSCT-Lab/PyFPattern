def merge(self, project_id, previous_group_id, new_group_id):
    self._send(project_id, 'merge', extra_data=({
        'project_id': project_id,
        'previous_group_id': previous_group_id,
        'new_group_id': new_group_id,
        'datetime': datetime.now(tz=pytz.utc),
    },), asynchronous=False)