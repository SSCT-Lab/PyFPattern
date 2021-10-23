def compute_phinorm(self, expElogthetad, expElogbetad):
    'Efficiently computes the normalizing factor in phi.'
    expElogtheta_sum = expElogthetad.sum(axis=0)
    phinorm = (expElogtheta_sum.dot(expElogbetad) + 1e-100)
    return phinorm