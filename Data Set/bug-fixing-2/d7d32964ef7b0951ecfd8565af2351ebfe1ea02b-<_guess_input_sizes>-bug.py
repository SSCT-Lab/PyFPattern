

def _guess_input_sizes(self, params_list):
    if hasattr(params_list[0], 'keys'):
        sizes = {
            
        }
        for params in params_list:
            for (k, value) in params.items():
                if value.input_size:
                    sizes[k] = value.input_size
        self.setinputsizes(**sizes)
    else:
        sizes = ([None] * len(params_list[0]))
        for params in params_list:
            for (i, value) in enumerate(params):
                if value.input_size:
                    sizes[i] = value.input_size
        self.setinputsizes(*sizes)
