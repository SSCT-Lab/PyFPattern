def iterator_postgres(self, chunk_size, batch_size=1000000):
    assert (self.days is not None)
    assert ((self.dtfield is not None) and (self.dtfield == self.order_by))
    dbc = connections[self.using]
    quote_name = dbc.ops.quote_name
    position = None
    cutoff = (timezone.now() - timedelta(days=self.days))
    with dbc.get_new_connection(dbc.get_connection_params()) as conn:
        conn.autocommit = False
        chunk = []
        completed = False
        while (not completed):
            with conn.cursor(uuid4().hex) as cursor:
                where = [('{} < %s'.format(quote_name(self.dtfield)), [cutoff])]
                if self.project_id:
                    where.append(('project_id = %s', [self.project_id]))
                if (self.order_by[0] == '-'):
                    direction = 'desc'
                    order_field = self.order_by[1:]
                    if (position is not None):
                        where.append(('{} <= %s'.format(quote_name(order_field)), [position]))
                else:
                    direction = 'asc'
                    order_field = self.order_by
                    if (position is not None):
                        where.append(('{} >= %s'.format(quote_name(order_field)), [position]))
                (conditions, parameters) = zip(*where)
                parameters = list(itertools.chain.from_iterable(parameters))
                query = '\n                        select id, {order_field}\n                        from {table}\n                        where {conditions}\n                        order by {order_field} {direction}\n                        limit {batch_size}\n                    '.format(table=self.model._meta.db_table, conditions=' and '.join(conditions), order_field=quote_name(order_field), direction=direction, batch_size=batch_size)
                cursor.execute(query, parameters)
                i = 0
                for (i, row) in enumerate(cursor, 1):
                    (key, position) = row
                    chunk.append(key)
                    if (len(chunk) == chunk_size):
                        (yield tuple(chunk))
                        chunk = []
                if (i < batch_size):
                    completed = True
            conn.commit()
        if chunk:
            (yield tuple(chunk))