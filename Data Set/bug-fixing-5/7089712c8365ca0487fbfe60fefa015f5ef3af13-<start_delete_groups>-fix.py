def start_delete_groups(self, project_id, group_ids):
    if (not group_ids):
        return
    state = {
        'transaction_id': uuid4().hex,
        'project_id': project_id,
        'group_ids': list(group_ids),
        'datetime': datetime.now(tz=pytz.utc),
    }
    self._send(project_id, 'start_delete_groups', extra_data=(state,), asynchronous=False)
    return state