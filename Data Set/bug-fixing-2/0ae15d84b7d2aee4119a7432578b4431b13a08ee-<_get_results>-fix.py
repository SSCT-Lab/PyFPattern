

def _get_results(self, hql, schema='default', fetch_size=None, hive_conf=None):
    from pyhive.exc import ProgrammingError
    if isinstance(hql, basestring):
        hql = [hql]
    previous_description = None
    with contextlib.closing(self.get_conn(schema)) as conn, contextlib.closing(conn.cursor()) as cur:
        cur.arraysize = (fetch_size or 1000)
        db = self.get_connection(self.hiveserver2_conn_id)
        if db.extra_dejson.get('run_set_variable_statements', True):
            env_context = get_context_from_env_var()
            if hive_conf:
                env_context.update(hive_conf)
            for (k, v) in env_context.items():
                cur.execute('set {}={}'.format(k, v))
        for statement in hql:
            cur.execute(statement)
            lowered_statement = statement.lower().strip()
            if (lowered_statement.startswith('select') or lowered_statement.startswith('with') or lowered_statement.startswith('show') or (lowered_statement.startswith('set') and ('=' not in lowered_statement))):
                description = [c for c in cur.description]
                if (previous_description and (previous_description != description)):
                    message = 'The statements are producing different descriptions:\n                                     Current: {}\n                                     Previous: {}'.format(repr(description), repr(previous_description))
                    raise ValueError(message)
                elif (not previous_description):
                    previous_description = description
                    (yield description)
                try:
                    for row in cur:
                        (yield row)
                except ProgrammingError:
                    self.log.debug('get_results returned no records')
