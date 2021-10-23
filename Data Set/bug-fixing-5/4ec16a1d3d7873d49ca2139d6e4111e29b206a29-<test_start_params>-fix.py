def test_start_params(self):
    (stat, inv) = (self.model.enforce_stationarity, self.model.enforce_invertibility)
    self.model.enforce_stationarity = False
    self.model.enforce_invertibility = False
    self.model.start_params
    (self.model.enforce_stationarity, self.model.enforce_invertibility) = (stat, inv)