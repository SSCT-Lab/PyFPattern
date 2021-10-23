

def updateParameters(self, learningRate):
    if (self.parameters() is not None):
        (params, gradParams) = self.parameters()
        if params:
            for (p, gp) in zip(params, gradParams):
                p.add_((- learningRate), gp)
