def _assert_success(res, desired_fun=None, desired_x=None, rtol=1e-08, atol=1e-08):
    assert_(res.success)
    assert_equal(res.status, 0)
    if (desired_fun is not None):
        assert_allclose(res.fun, desired_fun, err_msg='converged to an unexpected objective value', rtol=rtol, atol=atol)
    if (desired_x is not None):
        assert_allclose(res.x, desired_x, err_msg='converged to an unexpected solution', rtol=rtol, atol=atol)