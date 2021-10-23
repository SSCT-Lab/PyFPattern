def _beta_mle_a(a, b, n, s1):
    psiab = sc.psi((a + b))
    func = (s1 - (n * ((- psiab) + sc.psi(a))))
    return func