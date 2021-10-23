@contextlib.contextmanager
def _fork_rng(enabled=True):
    "\n    Forks the RNG, so that when you return, the RNG is reset\n    to the state that it was previously in.  This is important\n    if we are evaluating a trace twice, and it incorporates\n    randomness: if we don't reset the seed, we might get totally\n    different results!\n\n    TODO: Randomness in models is a big problem for reproduceability,\n    because it means if we start executing models out of order,\n    they may behave differently.  Interesting question is whether\n    or not backwards pass ever has randomness.  I hope not.\n    "
    if (not enabled):
        (yield)
        return
    cpu_rng_state = torch.get_rng_state()
    gpu_rng_state = None
    if torch.cuda.is_available():
        gpu_rng_state_all = torch.cuda.get_rng_state_all()
    (yield)
    torch.set_rng_state(cpu_rng_state)
    if (gpu_rng_state is not None):
        torch.cuda.set_rng_state_all(gpu_rng_state_all)