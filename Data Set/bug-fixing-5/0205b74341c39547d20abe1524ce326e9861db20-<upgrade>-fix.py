def upgrade():
    'Upgrade version.'
    json_type = sa.JSON
    conn = op.get_bind()
    if (conn.dialect.name != 'postgresql'):
        try:
            conn.execute('SELECT JSON_VALID(1)').fetchone()
        except (sa.exc.OperationalError, sa.exc.ProgrammingError):
            json_type = sa.Text
    op.create_table('serialized_dag', sa.Column('dag_id', sa.String(length=250), nullable=False), sa.Column('fileloc', sa.String(length=2000), nullable=False), sa.Column('fileloc_hash', sa.Integer(), nullable=False), sa.Column('data', json_type(), nullable=False), sa.Column('last_updated', sa.DateTime(), nullable=False), sa.PrimaryKeyConstraint('dag_id'))
    op.create_index('idx_fileloc_hash', 'serialized_dag', ['fileloc_hash'])
    if (conn.dialect.name == 'mysql'):
        conn.execute("SET time_zone = '+00:00'")
        cur = conn.execute('SELECT @@explicit_defaults_for_timestamp')
        res = cur.fetchall()
        if (res[0][0] == 0):
            raise Exception('Global variable explicit_defaults_for_timestamp needs to be on (1) for mysql')
        op.alter_column(table_name='serialized_dag', column_name='last_updated', type_=mysql.TIMESTAMP(fsp=6), nullable=False)
    else:
        if (conn.dialect.name in ('sqlite', 'mssql')):
            return
        if (conn.dialect.name == 'postgresql'):
            conn.execute('set timezone=UTC')
        op.alter_column(table_name='serialized_dag', column_name='last_updated', type_=sa.TIMESTAMP(timezone=True))