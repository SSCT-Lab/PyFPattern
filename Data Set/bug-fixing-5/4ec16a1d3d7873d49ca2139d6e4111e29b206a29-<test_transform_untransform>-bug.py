def test_transform_untransform(self):
    true_constrained = self.true_params
    self.model.update(self.true_params)
    contracted_polynomial_seasonal_ar = self.model.polynomial_seasonal_ar[self.model.polynomial_seasonal_ar.nonzero()]
    self.model.enforce_stationarity = (((self.model.k_ar == 0) or tools.is_invertible(np.r_[(1, (- self.model.polynomial_ar[1:]))])) and ((len(contracted_polynomial_seasonal_ar) <= 1) or tools.is_invertible(np.r_[(1, (- contracted_polynomial_seasonal_ar[1:]))])))
    contracted_polynomial_seasonal_ma = self.model.polynomial_seasonal_ma[self.model.polynomial_seasonal_ma.nonzero()]
    self.model.enforce_invertibility = (((self.model.k_ma == 0) or tools.is_invertible(np.r_[(1, (- self.model.polynomial_ma[1:]))])) and ((len(contracted_polynomial_seasonal_ma) <= 1) or tools.is_invertible(np.r_[(1, (- contracted_polynomial_seasonal_ma[1:]))])))
    unconstrained = self.model.untransform_params(true_constrained)
    constrained = self.model.transform_params(unconstrained)
    assert_almost_equal(constrained, true_constrained, 4)
    self.model.enforce_stationarity = True
    self.model.enforce_invertibility = True