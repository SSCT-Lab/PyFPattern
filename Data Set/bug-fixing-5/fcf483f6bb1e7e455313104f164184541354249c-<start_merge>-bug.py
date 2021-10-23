def start_merge(self, project_id, previous_group_ids, new_group_id):
    if (not previous_group_ids):
        return
    state = {
        'transaction_id': uuid4().hex,
        'project_id': project_id,
        'previous_group_ids': previous_group_ids,
        'new_group_id': new_group_id,
        'datetime': datetime.now(tz=pytz.utc),
    }
    self._send(project_id, 'start_merge', extra_data=(state,), asynchronous=False)