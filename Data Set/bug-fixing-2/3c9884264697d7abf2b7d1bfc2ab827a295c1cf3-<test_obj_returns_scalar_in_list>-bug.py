

def test_obj_returns_scalar_in_list(self):
    fmin_slsqp((lambda x: [0]), [1, 2, 3])
