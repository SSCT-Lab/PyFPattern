def bulk_delete_objects(model, limit=10000, transaction_id=None, logger=None, **filters):
    connection = connections[router.db_for_write(model)]
    quote_name = connection.ops.quote_name
    query = []
    params = []
    for (column, value) in filters.items():
        query.append(('%s = %%s' % (quote_name(column),)))
        params.append(value)
    if db.is_postgres():
        query = ('\n            delete from %(table)s\n            where id = any(array(\n                select id\n                from %(table)s\n                where (%(query)s)\n                limit %(limit)d\n            ))\n        ' % dict(query=' AND '.join(query), table=model._meta.db_table, limit=limit))
    elif db.is_mysql():
        query = ('\n            delete from %(table)s\n            where (%(query)s)\n            limit %(limit)d\n        ' % dict(query=' AND '.join(query), table=model._meta.db_table, limit=limit))
    else:
        if (logger is not None):
            logger.warning('Using slow deletion strategy due to unknown database')
        has_more = False
        for obj in model.objects.filter(**filters)[:limit]:
            obj.delete()
            has_more = True
        return has_more
    cursor = connection.cursor()
    cursor.execute(query, params)
    has_more = (cursor.rowcount > 0)
    if (has_more and (logger is not None)):
        logger.info('object.delete.bulk_executed', extra=dict((filters.items() + [('model', model.__name__), ('transaction_id', transaction_id)])))
    return has_more