def set_autocommit(self, conn, autocommit):
    '\n        Enable or disable autocommit for the given connection.\n\n        :param conn: The connection\n        :return:\n        '
    conn.jconn.setAutoCommit(autocommit)