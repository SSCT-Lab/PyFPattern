def lb_attributes_should_be_changed(target_lb, wished_lb):
    diff = {attr: wished_lb[attr] for attr in MUTABLE_ATTRIBUTES if (target_lb[attr] != wished_lb[attr])}
    if diff:
        return {attr: wished_lb[attr] for attr in MUTABLE_ATTRIBUTES}
    else:
        return diff