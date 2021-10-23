def _beta_mle_ab(theta, n, s1, s2):
    (a, b) = theta
    psiab = special.psi((a + b))
    func = [(s1 - (n * ((- psiab) + special.psi(a)))), (s2 - (n * ((- psiab) + special.psi(b))))]
    return func