def handler_launch_func(self, scope, handler):
    fetch_instance = handler
    period_secs = fetch_instance.period_secs
    var_name_to_key = {
        
    }
    for key in fetch_instance.var_dict:
        if isinstance(fetch_instance.var_dict[key], Variable):
            var_name_to_key[fetch_instance.var_dict[key].name] = key
        else:
            local_logger.warning('the value of {} is not a Variable'.format(key))
            var_name_to_key['None.var'] = key
    elapsed_secs = 0
    while True:
        self.running_lock.acquire()
        if (self.running == False):
            break
        if (elapsed_secs < period_secs):
            time.sleep(1)
            elapsed_secs += 1
        else:
            elapsed_secs = 0
            fetch_dict = {
                
            }
            for key in var_name_to_key:
                var = scope.find_var(key)
                fetch_dict[key] = var
                if (var == None):
                    local_logger.warning('{} value currently not available'.format(var_name_to_key[key]))
            res_dict = {
                
            }
            for key in fetch_dict:
                user_name = var_name_to_key[key]
                if (fetch_dict[key] == None):
                    res_dict[user_name] = None
                    continue
                else:
                    res_dict[user_name] = fetch_dict[key].get_tensor()
                lod = res_dict[user_name].lod()
                if (len(lod) > 0):
                    raise RuntimeError('Some of your fetched tensors                                             hold LoD information.                                             They can not be completely cast                                             to Python ndarray. We can                                             not return LoDTensor itself directly,                                             please choose another targets')
                if res_dict[user_name]._is_initialized():
                    res_dict[user_name] = np.array(res_dict[user_name])
                else:
                    res_dict[user_name] = None
            fetch_instance.handler(res_dict)
        self.running_lock.release()