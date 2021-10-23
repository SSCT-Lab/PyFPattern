def _beta_mle_ab(theta, n, s1, s2):
    (a, b) = theta
    psiab = sc.psi((a + b))
    func = [(s1 - (n * ((- psiab) + sc.psi(a)))), (s2 - (n * ((- psiab) + sc.psi(b))))]
    return func