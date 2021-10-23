def configure_adapters():
    from pendulum import Pendulum
    try:
        from sqlite3 import register_adapter
        register_adapter(Pendulum, (lambda val: val.isoformat(' ')))
    except ImportError:
        pass
    try:
        import MySQLdb.converters
        MySQLdb.converters.conversions[Pendulum] = MySQLdb.converters.DateTime2literal
    except ImportError:
        pass