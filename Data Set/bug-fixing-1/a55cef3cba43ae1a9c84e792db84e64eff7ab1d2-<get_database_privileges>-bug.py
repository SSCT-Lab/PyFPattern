

def get_database_privileges(cursor, user, db):
    priv_map = {
        'C': 'CREATE',
        'T': 'TEMPORARY',
        'c': 'CONNECT',
    }
    query = 'SELECT datacl FROM pg_database WHERE datname = %s'
    cursor.execute(query, (db,))
    datacl = cursor.fetchone()[0]
    if (datacl is None):
        return set()
    r = re.search(('%s=(C?T?c?)/[a-z]+\\,?' % user), datacl)
    if (r is None):
        return set()
    o = set()
    for v in r.group(1):
        o.add(priv_map[v])
    return normalize_privileges(o, 'database')
