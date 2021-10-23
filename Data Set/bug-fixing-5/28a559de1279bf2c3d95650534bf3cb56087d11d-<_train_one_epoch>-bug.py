def _train_one_epoch(self, context):
    '\n        Train one epoch.\n        '
    if context.skip_training:
        return
    executor = SlimGraphExecutor(self.place)
    if (context.optimize_graph.compiled_graph is None):
        context.optimize_graph.compiled_graph = compiler.CompiledProgram(context.optimize_graph.program).with_data_parallel(loss_name=context.optimize_graph.out_nodes['loss'])
    if (isinstance(context.train_reader, Variable) or (isinstance(context.train_reader, PyReader) and (not context.train_reader._iterable))):
        context.train_reader.start()
        try:
            while True:
                for strategy in self.strategies:
                    strategy.on_batch_begin(context)
                results = executor.run(context.optimize_graph, context.scope)
                results = [float(np.mean(result)) for result in results]
                if ((context.batch_id % self.log_period) == 0):
                    _logger.info('epoch:{}; batch_id:{}; {} = {}'.format(context.epoch_id, context.batch_id, context.optimize_graph.out_nodes.keys(), [round(r, 3) for r in results]))
                for strategy in self.strategies:
                    strategy.on_batch_end(context)
                context.batch_id += 1
        except EOFException:
            context.train_reader.reset()
    else:
        for data in context.train_reader():
            for strategy in self.strategies:
                strategy.on_batch_begin(context)
            results = executor.run(context.optimize_graph, context.scope, data=data)
            results = [float(np.mean(result)) for result in results]
            if ((context.batch_id % self.log_period) == 0):
                _logger.info('epoch:{}; batch_id:{}; {} = {}'.format(context.epoch_id, context.batch_id, context.optimize_graph.out_nodes.keys(), [round(r, 3) for r in results]))
            for strategy in self.strategies:
                strategy.on_batch_end(context)
            context.batch_id += 1
    context.batch_id = 0