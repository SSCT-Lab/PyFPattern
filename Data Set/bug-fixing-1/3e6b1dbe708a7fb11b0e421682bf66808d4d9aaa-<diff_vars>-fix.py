

def diff_vars(origin_vars, new_vars):
    global error
    var_error = False
    var_changed_error_massage = {
        
    }
    var_added_error_massage = []
    var_deleted_error_massage = []
    common_vars_name = (set(origin_vars.keys()) & set(new_vars.keys()))
    vars_name_only_in_origin = (set(origin_vars.keys()) - set(new_vars.keys()))
    vars_name_only_in_new = (set(new_vars.keys()) - set(origin_vars.keys()))
    for var_name in common_vars_name:
        if (cmp(origin_vars.get(var_name), new_vars.get(var_name)) == SAME):
            continue
        else:
            (error, var_error) = (True, True)
            var_changed_error_massage[var_name] = {
                
            }
            for arg_name in origin_vars.get(var_name):
                new_arg_value = new_vars.get(var_name, {
                    
                }).get(arg_name)
                origin_arg_value = origin_vars.get(var_name, {
                    
                }).get(arg_name)
                if (new_arg_value != origin_arg_value):
                    var_changed_error_massage[var_name][arg_name] = (origin_arg_value, new_arg_value)
    for var_name in vars_name_only_in_origin:
        (error, var_error) = (True, True)
        var_deleted_error_massage.append(var_name)
    for var_name in vars_name_only_in_new:
        if (not new_vars.get(var_name).get(DISPENSABLE)):
            (error, var_error) = (True, True)
            var_added_error_massage.append(var_name)
    var_diff_message = {
        
    }
    if var_added_error_massage:
        var_diff_message[ADD] = var_added_error_massage
    if var_changed_error_massage:
        var_diff_message[CHANGE] = var_changed_error_massage
    if var_deleted_error_massage:
        var_diff_message[DELETE] = var_deleted_error_massage
    return (var_error, var_diff_message)
