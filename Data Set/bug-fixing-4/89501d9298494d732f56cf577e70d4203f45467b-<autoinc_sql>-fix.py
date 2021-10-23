def autoinc_sql(self, table, column):
    args = {
        'sq_name': self._get_sequence_name(table),
        'tr_name': self._get_trigger_name(table),
        'tbl_name': self.quote_name(table),
        'col_name': self.quote_name(column),
    }
    sequence_sql = ('\nDECLARE\n    i INTEGER;\nBEGIN\n    SELECT COUNT(1) INTO i FROM USER_SEQUENCES\n        WHERE SEQUENCE_NAME = \'%(sq_name)s\';\n    IF i = 0 THEN\n        EXECUTE IMMEDIATE \'CREATE SEQUENCE "%(sq_name)s"\';\n    END IF;\nEND;\n/' % args)
    trigger_sql = ('\nCREATE OR REPLACE TRIGGER "%(tr_name)s"\nBEFORE INSERT ON %(tbl_name)s\nFOR EACH ROW\nWHEN (new.%(col_name)s IS NULL)\n    BEGIN\n        :new.%(col_name)s := "%(sq_name)s".nextval;\n    END;\n/' % args)
    return (sequence_sql, trigger_sql)