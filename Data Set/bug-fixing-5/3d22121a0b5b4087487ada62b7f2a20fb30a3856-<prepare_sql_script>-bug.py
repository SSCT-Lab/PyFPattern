def prepare_sql_script(self, sql):
    "\n        Take an SQL script that may contain multiple lines and return a list\n        of statements to feed to successive cursor.execute() calls.\n\n        Since few databases are able to process raw SQL scripts in a single\n        cursor.execute() call and PEP 249 doesn't talk about this use case,\n        the default implementation is conservative.\n        "
    try:
        import sqlparse
    except ImportError:
        raise ImproperlyConfigured("sqlparse is required if you don't split your SQL statements manually.")
    else:
        return [sqlparse.format(statement, strip_comments=True) for statement in sqlparse.split(sql) if statement]