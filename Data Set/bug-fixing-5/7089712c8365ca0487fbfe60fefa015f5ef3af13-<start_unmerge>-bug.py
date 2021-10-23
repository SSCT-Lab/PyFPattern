def start_unmerge(self, project_id, hashes, previous_group_id, new_group_id):
    if (not hashes):
        return
    state = {
        'transaction_id': uuid4().hex,
        'project_id': project_id,
        'previous_group_id': previous_group_id,
        'new_group_id': new_group_id,
        'hashes': hashes,
        'datetime': datetime.now(tz=pytz.utc),
    }
    self._send(project_id, 'start_unmerge', extra_data=(state,), asynchronous=False)
    return state