

def _take_2(seq):
    iterator = iter(seq)
    while True:
        n1 = next(iterator)
        n2 = next(iterator)
        (yield (n1, n2))
