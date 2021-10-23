def fetch_returned_insert_id(self, cursor):
    try:
        return int(cursor._insert_id_var.getvalue())
    except TypeError:
        raise DatabaseError('The database did not return a new row id. Probably "ORA-1403: no data found" was raised internally but was hidden by the Oracle OCI library (see https://code.djangoproject.com/ticket/28859).')