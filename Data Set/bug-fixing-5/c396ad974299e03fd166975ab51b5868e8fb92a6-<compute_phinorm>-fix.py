def compute_phinorm(self, expElogthetad, expElogbetad):
    'Efficiently computes the normalizing factor in phi.\n\n        Parameters\n        ----------\n        expElogthetad: numpy.ndarray\n            Value of variational distribution :math:`q(\theta|\\gamma)`.\n        expElogbetad: numpy.ndarray\n            Value of variational distribution :math:`q(\\beta|\\lambda)`.\n\n        Returns\n        -------\n        float\n            Value of normalizing factor.\n\n        '
    expElogtheta_sum = expElogthetad.sum(axis=0)
    phinorm = (expElogtheta_sum.dot(expElogbetad) + 1e-100)
    return phinorm