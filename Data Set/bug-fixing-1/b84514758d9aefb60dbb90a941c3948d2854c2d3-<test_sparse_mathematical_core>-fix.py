

@with_seed()
def test_sparse_mathematical_core():

    def util_sign(a):
        if np.isclose(a, (- 0), rtol=0.001, atol=0.001, equal_nan=True):
            return 0
        elif np.isclose(a, 0, rtol=0.001, atol=0.001, equal_nan=True):
            return 0
        elif (a < 0.0):
            return (- 1)
        else:
            return 1

    def check_binary_op_with_scalar(stype, output_grad_stype=None, input_grad_stype=None, density=0.5, ograd_density=0.5, force_overlap=False):
        check_sparse_mathematical_core('mul_scalar', stype, (lambda x, y: (x * y)), (lambda x, y: (x * y)), (lambda input, rhs: rhs), rhs_arg=5.0, data_init=2, grad_init=3, output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, density=density, ograd_density=ograd_density, force_overlap=force_overlap, verbose=False)
        check_sparse_mathematical_core('plus_scalar', stype, (lambda x, y: (x + y)), (lambda x, y: (x + y)), (lambda input, rhs: 1), rhs_arg=5.0, data_init=2, grad_init=3, output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, density=density, ograd_density=ograd_density, force_overlap=force_overlap, verbose=False)
        check_sparse_mathematical_core('minus_scalar', stype, (lambda x, y: (x - y)), (lambda x, y: (x - y)), (lambda input, rhs: 1), rhs_arg=5.0, data_init=2, grad_init=3, output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, density=density, ograd_density=ograd_density, force_overlap=force_overlap, verbose=False)

    def check_mathematical_core(stype, output_grad_stype=None, input_grad_stype=None, force_overlap=False, density=0.5, ograd_density=0.5):
        check_sparse_mathematical_core('negative', stype, (lambda x: mx.sym.sparse.negative(x)), (lambda x: np.negative(x)), force_overlap=force_overlap, density=density, input_grad_stype=input_grad_stype, ograd_density=ograd_density)
        check_sparse_mathematical_core('square', stype, (lambda x: mx.sym.sparse.square(x)), (lambda x: np.square(x)), (lambda x: (2 * x)), output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density, verbose=False)
        if (stype != 'csr'):
            check_sparse_mathematical_core('sqrt', stype, (lambda x: mx.sym.sparse.sqrt(x)), (lambda x: np.sqrt(x)), (lambda x: (1.0 / (2.0 * np.sqrt(x)))), output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density, verbose=False)
            check_sparse_mathematical_core('rsqrt', stype, (lambda x: mx.sym.sparse.rsqrt(x)), (lambda x: (1 / np.sqrt(x))), (lambda x: (- (1.0 / ((2.0 * x) * np.sqrt(x))))), output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('tan', stype, (lambda x: mx.sym.sparse.tan(x)), (lambda x: np.tan(x)), (lambda x: ((np.tan(x) ** 2) + 1)), output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('abs', stype, (lambda x: mx.sym.sparse.abs(x)), (lambda x: np.abs(x)), (lambda x: assign_each(x, function=util_sign)), output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('floor', stype, (lambda x: mx.sym.sparse.floor(x)), (lambda x: np.floor(x)), force_overlap=force_overlap, input_grad_stype=input_grad_stype, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('ceil', stype, (lambda x: mx.sym.sparse.ceil(x)), (lambda x: np.ceil(x)), force_overlap=force_overlap, input_grad_stype=input_grad_stype, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('sign', stype, (lambda x: mx.sym.sparse.sign(x)), (lambda x: np.sign(x)), (lambda x: np.zeros(x.shape)), output_grad_stype=output_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('cos', stype, (lambda x: mx.sym.sparse.cos(x)), (lambda x: np.cos(x)), (lambda x: (- np.sin(x))), output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('sin', stype, (lambda x: mx.sym.sparse.sin(x)), (lambda x: np.sin(x)), (lambda x: np.cos(x)), output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('arcsin', stype, (lambda x: mx.sym.sparse.arcsin(x)), (lambda x: np.arcsin(x)), (lambda x: (1.0 / ((1.0 - (x ** 2)) ** (1.0 / 2.0)))), data_init=0.5, grad_init=0.5, output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('arccos', stype, (lambda x: mx.sym.sparse.arccos(x)), (lambda x: np.arccos(x)), (lambda x: ((- 1.0) / ((1.0 - (x ** 2.0)) ** (1.0 / 2.0)))), data_init=0.5, grad_init=0.5, output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('arctan', stype, (lambda x: mx.sym.sparse.arctan(x)), (lambda x: np.arctan(x)), (lambda x: (1.0 / ((x ** 2.0) + 1.0))), data_init=0.5, grad_init=0.5, output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('degrees', stype, (lambda x: mx.sym.sparse.degrees(x)), (lambda x: np.degrees(x)), (lambda x: assign_each(x, (lambda a: (180.0 / np.pi)))), data_init=0.5, grad_init=0.5, output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('radians', stype, (lambda x: mx.sym.sparse.radians(x)), (lambda x: np.radians(x)), (lambda x: assign_each(x, (lambda a: (np.pi / 180.0)))), data_init=0.6, grad_init=1, output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('sinh', stype, (lambda x: mx.sym.sparse.sinh(x)), (lambda x: np.sinh(x)), (lambda x: np.cosh(x)), output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('cosh', stype, (lambda x: mx.sym.sparse.cosh(x)), (lambda x: np.cosh(x)), (lambda x: np.sinh(x)), data_init=5, grad_init=5, output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('tanh', stype, (lambda x: mx.sym.sparse.tanh(x)), (lambda x: np.tanh(x)), (lambda x: (1.0 - (np.tanh(x) ** 2))), data_init=0.5, grad_init=1, output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('arcsinh', stype, (lambda x: mx.sym.sparse.arcsinh(x)), (lambda x: np.arcsinh(x)), (lambda x: (1.0 / (((x ** 2) + 1.0) ** (1.0 / 2.0)))), output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('arccosh', stype, (lambda x: mx.sym.sparse.arccosh(x)), (lambda x: np.arccosh(x)), (lambda x: (1.0 / (((x ** 2) - 1.0) ** (1.0 / 2.0)))), output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('arctanh', stype, (lambda x: mx.sym.sparse.arctanh(x)), (lambda x: np.arctanh(x)), (lambda x: ((- 1.0) / ((x ** 2) - 1.0))), data_init=0.5, output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('log1p', stype, (lambda x: mx.sym.sparse.log1p(x)), (lambda x: np.log1p(x)), (lambda x: (1.0 / (1.0 + x))), data_init=0.5, grad_init=0.5, output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('expm1', stype, (lambda x: mx.sym.sparse.expm1(x)), (lambda x: np.expm1(x)), (lambda x: np.exp(x)), data_init=0.5, grad_init=0.5, output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('log10', stype, (lambda x: mx.sym.sparse.log10(x)), (lambda x: np.log10(x)), (lambda x: (1.0 / (x * np.log(10.0)))), output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('log2', stype, (lambda x: mx.sym.sparse.log2(x)), (lambda x: np.log2(x)), (lambda x: (1.0 / (x * np.log(2.0)))), output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            check_sparse_mathematical_core('rint', stype, (lambda x: mx.sym.sparse.rint(x)), (lambda x: np.rint(x)), force_overlap=force_overlap, density=density, input_grad_stype=input_grad_stype, ograd_density=ograd_density)
            check_sparse_mathematical_core('fix', stype, (lambda x: mx.sym.sparse.fix(x)), (lambda x: np.fix(x)), force_overlap=force_overlap, density=density, input_grad_stype=input_grad_stype, ograd_density=ograd_density)
            try:
                from scipy import special as scipy_special
                scipy_psi = np.vectorize((lambda x: (np.inf if (float(x).is_integer() and (x <= 0)) else scipy_special.psi(x))))
                check_sparse_mathematical_core('gamma', stype, (lambda x: mx.sym.sparse.gamma(x)), (lambda x: scipy_special.gamma(x)), (lambda x: (scipy_special.gamma(x) * scipy_psi(x))), output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
                check_sparse_mathematical_core('gammaln', stype, (lambda x: mx.sym.sparse.gammaln(x)), (lambda x: scipy_special.gammaln(x)), (lambda x: scipy_psi(x)), output_grad_stype=output_grad_stype, input_grad_stype=input_grad_stype, force_overlap=force_overlap, density=density, ograd_density=ograd_density)
            except ImportError:
                print('Could not import scipy. Skipping unit tests for special functions')
    for i in range(1):
        print('pass', i)
        for density in [0.0, random.uniform(0, 1), 1.0]:
            for ograd_density in [0.0, random.uniform(0, 1), 1.0]:
                for force_overlap in [False, True]:
                    print('{}, {}, {}'.format(density, ograd_density, force_overlap))
                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore')
                        check_mathematical_core('default', force_overlap=force_overlap, density=density, ograd_density=ograd_density)
                        check_mathematical_core('row_sparse', force_overlap=force_overlap, density=density, ograd_density=ograd_density)
                        check_mathematical_core('row_sparse', output_grad_stype='default', force_overlap=force_overlap, density=density, ograd_density=ograd_density)
                        check_mathematical_core('row_sparse', output_grad_stype='row_sparse', force_overlap=force_overlap, density=density, ograd_density=ograd_density)
                        check_mathematical_core('csr', output_grad_stype='default', force_overlap=force_overlap, density=density, ograd_density=ograd_density)
                        check_mathematical_core('csr', output_grad_stype='csr', force_overlap=force_overlap, density=density, ograd_density=ograd_density)
                        check_binary_op_with_scalar('default', density=density, ograd_density=ograd_density, force_overlap=force_overlap)
                        check_binary_op_with_scalar('row_sparse', density=density, ograd_density=ograd_density, force_overlap=force_overlap)
                        check_binary_op_with_scalar('row_sparse', output_grad_stype='default', density=density, ograd_density=ograd_density, force_overlap=force_overlap)
                        check_binary_op_with_scalar('row_sparse', output_grad_stype='row_sparse', density=density, ograd_density=ograd_density, force_overlap=force_overlap)
                        check_binary_op_with_scalar('csr', output_grad_stype='csr', input_grad_stype='default', density=density, ograd_density=ograd_density, force_overlap=force_overlap)
                        check_binary_op_with_scalar('csr', output_grad_stype='csr', input_grad_stype='csr', density=density, ograd_density=ograd_density, force_overlap=force_overlap)
                        check_binary_op_with_scalar('csr', output_grad_stype='default', density=density, ograd_density=ograd_density, force_overlap=force_overlap)
