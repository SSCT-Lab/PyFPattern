

def diff_attr(ori_attrs, new_attrs):
    global error
    attr_error = False
    attr_changed_error_massage = {
        
    }
    attr_added_error_massage = []
    attr_deleted_error_massage = []
    common_attrs = (set(ori_attrs.keys()) & set(new_attrs.keys()))
    attrs_only_in_origin = (set(ori_attrs.keys()) - set(new_attrs.keys()))
    attrs_only_in_new = (set(new_attrs.keys()) - set(ori_attrs.keys()))
    for attr_name in common_attrs:
        if (cmp(ori_attrs.get(attr_name), new_attrs.get(attr_name)) == SAME):
            continue
        else:
            (error, attr_error) = (True, True)
            attr_changed_error_massage[attr_name] = {
                
            }
            for arg_name in ori_attrs.get(attr_name):
                new_arg_value = new_attrs.get(attr_name, {
                    
                }).get(arg_name)
                origin_arg_value = ori_attrs.get(attr_name, {
                    
                }).get(arg_name)
                if (new_arg_value != origin_arg_value):
                    attr_changed_error_massage[attr_name][arg_name] = (origin_arg_value, new_arg_value)
    for attr_name in attrs_only_in_origin:
        (error, attr_error) = (True, True)
        attr_deleted_error_massage.append(attr_name)
    for attr_name in attrs_only_in_new:
        if (new_attrs.get(attr_name).get(DEFAULT_VALUE) == None):
            (error, attr_error) = (True, True)
            attr_added_error_massage.append(attr_name)
    attr_diff_message = {
        
    }
    if attr_added_error_massage:
        attr_diff_message[ADD] = attr_added_error_massage
    if attr_changed_error_massage:
        attr_diff_message[CHANGE] = attr_changed_error_massage
    if attr_deleted_error_massage:
        attr_diff_message[DELETE] = attr_deleted_error_massage
    return (attr_error, attr_diff_message)
