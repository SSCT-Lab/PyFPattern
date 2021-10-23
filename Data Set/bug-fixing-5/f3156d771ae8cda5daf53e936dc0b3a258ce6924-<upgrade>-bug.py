def upgrade():
    op.drop_table('chart')
    op.drop_table('users')