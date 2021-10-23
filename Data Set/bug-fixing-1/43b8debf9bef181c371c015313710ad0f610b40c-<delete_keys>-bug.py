

def delete_keys(session, to_delete, check_mode):
    if check_mode:
        return
    for key in to_delete:
        session.request('DELETE', (API_BASE + ('/user/keys/%s' % key[id])))
