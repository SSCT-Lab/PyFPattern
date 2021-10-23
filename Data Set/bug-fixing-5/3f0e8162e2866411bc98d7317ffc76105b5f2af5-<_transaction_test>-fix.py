def _transaction_test(self):
    with self.pandasSQL.run_transaction() as trans:
        trans.execute('CREATE TABLE test_trans (A INT, B TEXT)')
    ins_sql = "INSERT INTO test_trans (A,B) VALUES (1, 'blah')"
    try:
        with self.pandasSQL.run_transaction() as trans:
            trans.execute(ins_sql)
            raise Exception('error')
    except Exception:
        pass
    res = self.pandasSQL.read_query('SELECT * FROM test_trans')
    assert (len(res) == 0)
    with self.pandasSQL.run_transaction() as trans:
        trans.execute(ins_sql)
    res2 = self.pandasSQL.read_query('SELECT * FROM test_trans')
    assert (len(res2) == 1)