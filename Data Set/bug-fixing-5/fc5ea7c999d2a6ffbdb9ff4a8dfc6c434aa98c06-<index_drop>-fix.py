def index_drop(cursor, module, idxname, concurrent=True):
    'Drop index'
    changed = False
    if (not index_exists(cursor, idxname)):
        return changed
    mode = 'CONCURRENTLY'
    if (not concurrent):
        mode = ''
    query = ('DROP INDEX %s %s' % (mode, idxname))
    try:
        cursor.execute(query)
        changed = True
    except psycopg2.InternalError as e:
        if (e.pgcode == '25006'):
            changed = False
            module.fail_json(msg=e.pgerror, exception=traceback.format_exc())
        else:
            raise psycopg2.InternalError(e)
    return changed