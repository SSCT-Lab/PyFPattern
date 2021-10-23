def test_start_params(self):
    self.model.enforce_stationarity = False
    self.model.enforce_invertibility = False
    self.model.start_params
    self.model.enforce_stationarity = True
    self.model.enforce_invertibility = True