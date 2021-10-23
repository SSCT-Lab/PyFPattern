

def func_reconstruct_closure(values):
    'Deserialization helper that reconstructs a closure.'
    nums = range(len(values))
    src = ['def func(arg):']
    src += [('  _%d = arg[%d]' % (n, n)) for n in nums]
    src += [('  return lambda:(%s)' % ','.join([('_%d' % n) for n in nums])), '']
    src = '\n'.join(src)
    try:
        exec(src)
    except:
        raise SyntaxError(src)
    return func(values).__closure__
