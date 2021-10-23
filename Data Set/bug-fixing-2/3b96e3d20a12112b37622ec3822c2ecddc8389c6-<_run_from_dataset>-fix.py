

def _run_from_dataset(self, program=None, dataset=None, scope=None, thread=0, is_infer=False, debug=False, fetch_list=None, fetch_info=None, print_period=100, fetch_handler=None):
    if (dataset is None):
        raise RuntimeError('dataset is need and should be initialized')
    if program._pipeline_opt:
        thread = self._adjust_pipeline_resource(program._pipeline_opt, dataset, thread)
    dataset._prepare_to_run()
    (scope, trainer) = self._prepare_trainer(program=program, dataset=dataset, scope=scope, thread=thread, debug=debug, fetch_list=fetch_list, fetch_info=fetch_info, print_period=print_period)
    trainer._set_infer(is_infer)
    trainer._gen_trainer_desc()
    self._dump_debug_info(program=program, trainer=trainer)
    dataset._dynamic_adjust_before_train(trainer.proto_desc.thread_num)
    trainer_instance = self._default_executor.init_for_dataset(program.desc, trainer._desc(), scope, dataset.dataset)
    if (fetch_handler is not None):
        scope0 = trainer_instance.get_worker_scope(0)
        fetch_monitor = FetchHandlerMonitor(scope0, fetch_handler)
        fetch_monitor.start()
        self._default_executor.run_from_dataset(trainer_instance)
        fetch_monitor.stop()
    else:
        self._default_executor.run_from_dataset(trainer_instance)
    dataset._dynamic_adjust_after_train()
    dataset._finish_to_run()
    return None
