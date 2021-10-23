def filter_sk_params(self, fn, override=None):
    "Filters `sk_params` and return those in `fn`'s arguments.\n\n        # Arguments\n            fn : arbitrary function\n            override: dictionary, values to override sk_params\n\n        # Returns\n            res : dictionary dictionary containing variables\n                in both sk_params and fn's arguments.\n        "
    override = (override or {
        
    })
    res = {
        
    }
    for (name, value) in self.sk_params.items():
        if has_arg(fn, name):
            res.update({
                name: value,
            })
    res.update(override)
    return res