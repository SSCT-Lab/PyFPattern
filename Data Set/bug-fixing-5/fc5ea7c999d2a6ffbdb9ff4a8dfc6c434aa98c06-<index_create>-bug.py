def index_create(cursor, module, idxname, tblname, idxtype, columns, cond, concurrent=True):
    'Create new index'
    changed = False
    if (idxtype is None):
        idxtype = 'BTREE'
    mode = 'CONCURRENTLY'
    if (not concurrent):
        mode = ''
    if (cond is None):
        condition = ''
    else:
        condition = ('WHERE %s' % cond)
    if (cond is not None):
        cond = (' WHERE %s' % cond)
    for column in columns.split(','):
        column.strip()
    query = ('CREATE INDEX %s %s ON %s USING %s (%s)%s' % (mode, idxname, tblname, idxtype, columns, condition))
    try:
        if index_exists(cursor, idxname):
            return False
        cursor.execute(query)
        changed = True
    except psycopg2.InternalError as e:
        if (e.pgcode == '25006'):
            changed = False
            module.fail_json(msg=e.pgerror, exception=traceback.format_exc())
            return changed
        else:
            raise psycopg2.InternalError(e)
    return changed