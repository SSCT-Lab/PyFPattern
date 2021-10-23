def add_data_norm_table(self, table_id, learning_rate, param_var, grad_var, strategy, sparse_table_names):
    '\n        Args:\n            table_id(int): id of datanorm table\n            strategy(dict): the datanorm config dict.\n        Returns:\n            return None \n        '
    fea_dim = 0
    dense_param_vars = []
    for p in param_var:
        if (p.name not in sparse_table_names):
            dense_param_vars.append(p)
    for param in dense_param_vars:
        fea_dim += reduce((lambda x, y: (x * y)), param.shape, 1)
    for table in self._server.downpour_server_param.downpour_table_param:
        if (table.table_id == table_id):
            if (table.type == pslib.PS_DENSE_TABLE):
                table.accessor.fea_dim = fea_dim
                return
            else:
                raise ValueError(('expect table %s type=%s, but actual type=%s' % (table_id, pslib.PS_DENSE_TABLE, table.type)))
    if (strategy is None):
        strategy = dict()
    support_datanorm_key_list = ['datanorm_table_class', 'datanorm_compress_in_save', 'datanorm_accessor_class', 'datanorm_operation', 'datanorm_decay_rate']
    for key in strategy:
        if (key not in support_datanorm_key_list):
            raise ValueError(("strategy key '%s' not support" % key))
    table = self._server.downpour_server_param.downpour_table_param.add()
    table.table_id = table_id
    table.table_class = strategy.get('datanorm_table_class', 'DownpourDenseTable')
    table.type = pslib.PS_DENSE_TABLE
    table.compress_in_save = strategy.get('datanorm_compress_in_save', True)
    table.accessor.accessor_class = strategy.get('datanorm_accessor_class', 'DownpourDenseValueAccessor')
    table.accessor.dense_sgd_param.name = strategy.get('datanorm_operation', 'summary')
    table.accessor.dense_sgd_param.summary.summary_decay_rate = strategy.get('datanorm_decay_rate', 0.999999)
    table.accessor.fea_dim = fea_dim