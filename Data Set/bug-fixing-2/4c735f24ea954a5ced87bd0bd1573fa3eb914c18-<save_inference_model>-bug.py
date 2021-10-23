

def save_inference_model(self, executor, dirname, feeded_var_names, target_vars, main_program=None, export_for_deployment=True):
    '\n        Prune the given `main_program` to build a new program especially for inference,\n        and then save it and all related parameters to given `dirname` by the `executor`.\n        '
    if (main_program is not None):
        io.save_inference_model(dirname, feeded_var_names, target_vars, executor, main_program, None, None, export_for_deployment)
    else:
        io.save_inference_model(dirname, feeded_var_names, target_vars, executor, self._origin_program, None, None, export_for_deployment, model_only=True)
        model_basename = '__model__'
        model_filename = os.path.join(dirname, model_basename)
        with open(model_filename, 'rb') as f:
            program_desc_str = f.read()
        program = Program.parse_from_string(program_desc_str)
        program._copy_dist_param_info_from(self.main_program)
        self.save_persistables(executor, dirname, program)
