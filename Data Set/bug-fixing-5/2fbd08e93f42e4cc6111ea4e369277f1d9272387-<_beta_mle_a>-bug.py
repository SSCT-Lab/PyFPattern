def _beta_mle_a(a, b, n, s1):
    psiab = special.psi((a + b))
    func = (s1 - (n * ((- psiab) + special.psi(a))))
    return func