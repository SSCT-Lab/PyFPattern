

@classmethod
def type_map(cls, mysql_type):
    t = MySQLdb.constants.FIELD_TYPE
    d = {
        t.BIT: 'INT',
        t.DECIMAL: 'DOUBLE',
        t.DOUBLE: 'DOUBLE',
        t.FLOAT: 'DOUBLE',
        t.INT24: 'INT',
        t.LONG: 'BIGINT',
        t.LONGLONG: 'DECIMAL(38,0)',
        t.SHORT: 'INT',
        t.TINY: 'SMALLINT',
        t.YEAR: 'INT',
        t.TIMESTAMP: 'TIMESTAMP',
    }
    return (d[mysql_type] if (mysql_type in d) else 'STRING')
