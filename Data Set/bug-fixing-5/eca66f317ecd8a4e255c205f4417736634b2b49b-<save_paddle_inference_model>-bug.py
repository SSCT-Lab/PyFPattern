def save_paddle_inference_model(self, executor, scope, program, feeded_vars, target_vars, output_path, day, pass_id, hadoop_fs_name, hadoop_fs_ugi, hadoop_home='$HADOOP_HOME', save_combine=True):
    '\n        save paddle inference model, and upload to hdfs dnn_plugin path\n\n        Args:\n            executor(Executor): fluid Executor\n            scope(Scope): fluid Scope\n            program(Program): fluid Program\n            feeded_vars(list[Variable]): feed vars\n            target_vars(list[variable]): fetch vars\n            output_path(str): hdfs/afs output path\n            day(str|int): training day\n            pass_id(str|int): training pass\n            hadoop_fs_name(str): hadoop fs name\n            hadoop_fs_ugi(str): hadoop fs ugi\n            hadoop_home(str): hadoop home, default is "$HADOOP_HOME"\n            save_combine(bool): whether to save in a file or seperate files,\n                                default is True\n\n        Examples:\n            .. code-block:: python\n\n              from paddle.fluid.incubate.fleet.utils.fleet_util import FleetUtil\n              fleet_util = FleetUtil()\n              fleet_util.save_paddle_inference_model(exe,\n                                                     join_scope,\n                                                     join_program,\n                                                     feeded_vars,\n                                                     target_vars,\n                                                     "hdfs:/my/output/path/",\n                                                     day=20190727,\n                                                     pass_id=6,\n                                                     hadoop_fs_name="xxx",\n                                                     hadoop_fs_ugi="xxx,xxx")\n        '
    day = str(day)
    pass_id = str(pass_id)
    feeded_var_names = [i.name for i in feeded_vars]
    model_name = 'inference_model'
    self.pull_all_dense_params(scope, program)
    if (fleet.worker_index() == 0):
        with fluid.scope_guard(scope):
            if save_combine:
                fluid.io.save_inference_model(dirname=model_name, feeded_var_names=feeded_var_names, target_vars=target_vars, executor=exe, main_program=program, params_filename='params')
            else:
                fluid.io.save_inference_model(dirname=model_name, feeded_var_names=feeded_var_names, target_vars=target_vars, executor=exe, main_program=program)
        configs = {
            'fs.default.name': hadoop_fs_name,
            'hadoop.job.ugi': hadoop_fs_ugi,
        }
        client = HDFSClient(hadoop_home, configs)
        if (pass_id == '-1'):
            dest = ('%s/%s/base/dnn_plugin/' % (output_path, day))
        else:
            dest = ('%s/%s/delta-%s/dnn_plugin/' % (output_path, day, pass_id))
        if (not client.is_exist(dest)):
            client.makedirs(dest)
        client.upload(dest, model_name)
    fleet._role_maker._barrier_worker()