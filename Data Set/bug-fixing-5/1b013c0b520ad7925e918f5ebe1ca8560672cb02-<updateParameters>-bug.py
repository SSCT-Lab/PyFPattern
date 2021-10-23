def updateParameters(self, learningRate):
    (params, gradParams) = self.parameters()
    if params:
        for (p, gp) in zip(params, gradParams):
            p.add_((- learningRate), gp)