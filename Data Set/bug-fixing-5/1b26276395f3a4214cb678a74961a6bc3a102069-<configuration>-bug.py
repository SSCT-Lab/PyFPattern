def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration, dot_join
    from numpy.distutils.system_info import get_info
    config = Configuration('core', parent_package, top_path)
    local_dir = config.local_path
    codegen_dir = join(local_dir, 'code_generators')
    if is_released(config):
        warnings.simplefilter('error', MismatchCAPIWarning)
    check_api_version(C_API_VERSION, codegen_dir)
    generate_umath_py = join(codegen_dir, 'generate_umath.py')
    n = dot_join(config.name, 'generate_umath')
    generate_umath = npy_load_module('_'.join(n.split('.')), generate_umath_py, ('.py', 'U', 1))
    header_dir = 'include/numpy'
    cocache = CallOnceOnly()

    def generate_config_h(ext, build_dir):
        target = join(build_dir, header_dir, 'config.h')
        d = os.path.dirname(target)
        if (not os.path.exists(d)):
            os.makedirs(d)
        if newer(__file__, target):
            config_cmd = config.get_config_cmd()
            log.info('Generating %s', target)
            (moredefs, ignored) = cocache.check_types(config_cmd, ext, build_dir)
            mathlibs = check_mathlib(config_cmd)
            moredefs.append(('MATHLIB', ','.join(mathlibs)))
            check_math_capabilities(config_cmd, moredefs, mathlibs)
            moredefs.extend(cocache.check_ieee_macros(config_cmd)[0])
            moredefs.extend(cocache.check_complex(config_cmd, mathlibs)[0])
            if is_npy_no_signal():
                moredefs.append('__NPY_PRIVATE_NO_SIGNAL')
            if ((sys.platform == 'win32') or (os.name == 'nt')):
                win32_checks(moredefs)
            moredefs.append(('NPY_RESTRICT', config_cmd.check_restrict()))
            inline = config_cmd.check_inline()
            if NPY_RELAXED_STRIDES_CHECKING:
                moredefs.append(('NPY_RELAXED_STRIDES_CHECKING', 1))
            if NPY_RELAXED_STRIDES_DEBUG:
                moredefs.append(('NPY_RELAXED_STRIDES_DEBUG', 1))
            rep = check_long_double_representation(config_cmd)
            moredefs.append((('HAVE_LDOUBLE_%s' % rep), 1))
            if (sys.version_info[0] == 3):
                moredefs.append(('NPY_PY3K', 1))
            target_f = open(target, 'w')
            for d in moredefs:
                if isinstance(d, str):
                    target_f.write(('#define %s\n' % d))
                else:
                    target_f.write(('#define %s %s\n' % (d[0], d[1])))
            target_f.write('#ifndef __cplusplus\n')
            if (inline == 'inline'):
                target_f.write('/* #undef inline */\n')
            else:
                target_f.write(('#define inline %s\n' % inline))
            target_f.write('#endif\n')
            target_f.write('\n#ifndef _NPY_NPY_CONFIG_H_\n#error config.h should never be included directly, include npy_config.h instead\n#endif\n')
            target_f.close()
            print('File:', target)
            target_f = open(target)
            print(target_f.read())
            target_f.close()
            print('EOF')
        else:
            mathlibs = []
            target_f = open(target)
            for line in target_f:
                s = '#define MATHLIB'
                if line.startswith(s):
                    value = line[len(s):].strip()
                    if value:
                        mathlibs.extend(value.split(','))
            target_f.close()
        if hasattr(ext, 'libraries'):
            ext.libraries.extend(mathlibs)
        incl_dir = os.path.dirname(target)
        if (incl_dir not in config.numpy_include_dirs):
            config.numpy_include_dirs.append(incl_dir)
        return target

    def generate_numpyconfig_h(ext, build_dir):
        'Depends on config.h: generate_config_h has to be called before !'
        config.add_include_dirs(join(build_dir, 'src', 'common'))
        config.add_include_dirs(join(build_dir, 'src', 'npymath'))
        target = join(build_dir, header_dir, '_numpyconfig.h')
        d = os.path.dirname(target)
        if (not os.path.exists(d)):
            os.makedirs(d)
        if newer(__file__, target):
            config_cmd = config.get_config_cmd()
            log.info('Generating %s', target)
            (ignored, moredefs) = cocache.check_types(config_cmd, ext, build_dir)
            if is_npy_no_signal():
                moredefs.append(('NPY_NO_SIGNAL', 1))
            if is_npy_no_smp():
                moredefs.append(('NPY_NO_SMP', 1))
            else:
                moredefs.append(('NPY_NO_SMP', 0))
            mathlibs = check_mathlib(config_cmd)
            moredefs.extend(cocache.check_ieee_macros(config_cmd)[1])
            moredefs.extend(cocache.check_complex(config_cmd, mathlibs)[1])
            if NPY_RELAXED_STRIDES_CHECKING:
                moredefs.append(('NPY_RELAXED_STRIDES_CHECKING', 1))
            if NPY_RELAXED_STRIDES_DEBUG:
                moredefs.append(('NPY_RELAXED_STRIDES_DEBUG', 1))
            if config_cmd.check_decl('PRIdPTR', headers=['inttypes.h']):
                moredefs.append(('NPY_USE_C99_FORMATS', 1))
            hidden_visibility = visibility_define(config_cmd)
            moredefs.append(('NPY_VISIBILITY_HIDDEN', hidden_visibility))
            moredefs.append(('NPY_ABI_VERSION', ('0x%.8X' % C_ABI_VERSION)))
            moredefs.append(('NPY_API_VERSION', ('0x%.8X' % C_API_VERSION)))
            target_f = open(target, 'w')
            for d in moredefs:
                if isinstance(d, str):
                    target_f.write(('#define %s\n' % d))
                else:
                    target_f.write(('#define %s %s\n' % (d[0], d[1])))
            target_f.write('\n#ifndef __STDC_FORMAT_MACROS\n#define __STDC_FORMAT_MACROS 1\n#endif\n')
            target_f.close()
            print(('File: %s' % target))
            target_f = open(target)
            print(target_f.read())
            target_f.close()
            print('EOF')
        config.add_data_files((header_dir, target))
        return target

    def generate_api_func(module_name):

        def generate_api(ext, build_dir):
            script = join(codegen_dir, (module_name + '.py'))
            sys.path.insert(0, codegen_dir)
            try:
                m = __import__(module_name)
                log.info('executing %s', script)
                (h_file, c_file, doc_file) = m.generate_api(os.path.join(build_dir, header_dir))
            finally:
                del sys.path[0]
            config.add_data_files((header_dir, h_file), (header_dir, doc_file))
            return (h_file,)
        return generate_api
    generate_numpy_api = generate_api_func('generate_numpy_api')
    generate_ufunc_api = generate_api_func('generate_ufunc_api')
    config.add_include_dirs(join(local_dir, 'src', 'common'))
    config.add_include_dirs(join(local_dir, 'src'))
    config.add_include_dirs(join(local_dir))
    config.add_data_files('include/numpy/*.h')
    config.add_include_dirs(join('src', 'npymath'))
    config.add_include_dirs(join('src', 'multiarray'))
    config.add_include_dirs(join('src', 'umath'))
    config.add_include_dirs(join('src', 'npysort'))
    config.add_define_macros([('NPY_INTERNAL_BUILD', '1')])
    config.add_define_macros([('HAVE_NPY_CONFIG_H', '1')])
    if (sys.platform[:3] == 'aix'):
        config.add_define_macros([('_LARGE_FILES', None)])
    else:
        config.add_define_macros([('_FILE_OFFSET_BITS', '64')])
        config.add_define_macros([('_LARGEFILE_SOURCE', '1')])
        config.add_define_macros([('_LARGEFILE64_SOURCE', '1')])
    config.numpy_include_dirs.extend(config.paths('include'))
    deps = [join('src', 'npymath', '_signbit.c'), join('include', 'numpy', '*object.h'), join(codegen_dir, 'genapi.py')]
    config.add_extension('_dummy', sources=[join('src', 'dummymodule.c'), generate_config_h, generate_numpyconfig_h, generate_numpy_api])
    subst_dict = dict([('sep', os.path.sep), ('pkgname', 'numpy.core')])

    def get_mathlib_info(*args):
        config_cmd = config.get_config_cmd()
        st = config_cmd.try_link('int main(void) { return 0;}')
        if (not st):
            raise RuntimeError('Broken toolchain: cannot link a simple C program')
        mlibs = check_mathlib(config_cmd)
        posix_mlib = ' '.join([('-l%s' % l) for l in mlibs])
        msvc_mlib = ' '.join([('%s.lib' % l) for l in mlibs])
        subst_dict['posix_mathlib'] = posix_mlib
        subst_dict['msvc_mathlib'] = msvc_mlib
    npymath_sources = [join('src', 'npymath', 'npy_math_internal.h.src'), join('src', 'npymath', 'npy_math.c'), join('src', 'npymath', 'ieee754.c.src'), join('src', 'npymath', 'npy_math_complex.c.src'), join('src', 'npymath', 'halffloat.c')]
    is_msvc = (platform.platform().startswith('Windows') and platform.python_compiler().startswith('MS'))
    config.add_installed_library('npymath', sources=(npymath_sources + [get_mathlib_info]), install_dir='lib', build_info={
        'include_dirs': [],
        'extra_compiler_args': (['/GL-'] if is_msvc else []),
    })
    config.add_npy_pkg_config('npymath.ini.in', 'lib/npy-pkg-config', subst_dict)
    config.add_npy_pkg_config('mlib.ini.in', 'lib/npy-pkg-config', subst_dict)
    npysort_sources = [join('src', 'common', 'npy_sort.h.src'), join('src', 'npysort', 'quicksort.c.src'), join('src', 'npysort', 'mergesort.c.src'), join('src', 'npysort', 'timsort.c.src'), join('src', 'npysort', 'heapsort.c.src'), join('src', 'npysort', 'radixsort.c.src'), join('src', 'common', 'npy_partition.h.src'), join('src', 'npysort', 'selection.c.src'), join('src', 'common', 'npy_binsearch.h.src'), join('src', 'npysort', 'binsearch.c.src')]
    config.add_library('npysort', sources=npysort_sources, include_dirs=[])
    config.add_extension('_multiarray_tests', sources=[join('src', 'multiarray', '_multiarray_tests.c.src'), join('src', 'common', 'mem_overlap.c')], depends=[join('src', 'common', 'mem_overlap.h'), join('src', 'common', 'npy_extint128.h')], libraries=['npymath'])
    common_deps = [join('src', 'common', 'array_assign.h'), join('src', 'common', 'binop_override.h'), join('src', 'common', 'cblasfuncs.h'), join('src', 'common', 'lowlevel_strided_loops.h'), join('src', 'common', 'mem_overlap.h'), join('src', 'common', 'npy_cblas.h'), join('src', 'common', 'npy_config.h'), join('src', 'common', 'npy_ctypes.h'), join('src', 'common', 'npy_extint128.h'), join('src', 'common', 'npy_import.h'), join('src', 'common', 'npy_longdouble.h'), join('src', 'common', 'templ_common.h.src'), join('src', 'common', 'ucsnarrow.h'), join('src', 'common', 'ufunc_override.h'), join('src', 'common', 'umathmodule.h'), join('src', 'common', 'numpyos.h')]
    common_src = [join('src', 'common', 'array_assign.c'), join('src', 'common', 'mem_overlap.c'), join('src', 'common', 'npy_longdouble.c'), join('src', 'common', 'templ_common.h.src'), join('src', 'common', 'ucsnarrow.c'), join('src', 'common', 'ufunc_override.c'), join('src', 'common', 'numpyos.c')]
    blas_info = get_info('blas_opt', 0)
    if (blas_info and (('HAVE_CBLAS', None) in blas_info.get('define_macros', []))):
        extra_info = blas_info
        common_src.extend([join('src', 'common', 'cblasfuncs.c'), join('src', 'common', 'python_xerbla.c')])
        if uses_accelerate_framework(blas_info):
            common_src.extend(get_sgemv_fix())
    else:
        extra_info = {
            
        }
    multiarray_deps = (([join('src', 'multiarray', 'arrayobject.h'), join('src', 'multiarray', 'arraytypes.h'), join('src', 'multiarray', 'arrayfunction_override.h'), join('src', 'multiarray', 'buffer.h'), join('src', 'multiarray', 'calculation.h'), join('src', 'multiarray', 'common.h'), join('src', 'multiarray', 'convert_datatype.h'), join('src', 'multiarray', 'convert.h'), join('src', 'multiarray', 'conversion_utils.h'), join('src', 'multiarray', 'ctors.h'), join('src', 'multiarray', 'descriptor.h'), join('src', 'multiarray', 'dragon4.h'), join('src', 'multiarray', 'getset.h'), join('src', 'multiarray', 'hashdescr.h'), join('src', 'multiarray', 'iterators.h'), join('src', 'multiarray', 'mapping.h'), join('src', 'multiarray', 'methods.h'), join('src', 'multiarray', 'multiarraymodule.h'), join('src', 'multiarray', 'nditer_impl.h'), join('src', 'multiarray', 'number.h'), join('src', 'multiarray', 'refcount.h'), join('src', 'multiarray', 'scalartypes.h'), join('src', 'multiarray', 'sequence.h'), join('src', 'multiarray', 'shape.h'), join('src', 'multiarray', 'strfuncs.h'), join('src', 'multiarray', 'typeinfo.h'), join('src', 'multiarray', 'usertypes.h'), join('src', 'multiarray', 'vdot.h'), join('include', 'numpy', 'arrayobject.h'), join('include', 'numpy', '_neighborhood_iterator_imp.h'), join('include', 'numpy', 'npy_endian.h'), join('include', 'numpy', 'arrayscalars.h'), join('include', 'numpy', 'noprefix.h'), join('include', 'numpy', 'npy_interrupt.h'), join('include', 'numpy', 'npy_3kcompat.h'), join('include', 'numpy', 'npy_math.h'), join('include', 'numpy', 'halffloat.h'), join('include', 'numpy', 'npy_common.h'), join('include', 'numpy', 'npy_os.h'), join('include', 'numpy', 'utils.h'), join('include', 'numpy', 'ndarrayobject.h'), join('include', 'numpy', 'npy_cpu.h'), join('include', 'numpy', 'numpyconfig.h'), join('include', 'numpy', 'ndarraytypes.h'), join('include', 'numpy', 'npy_1_7_deprecated_api.h')] + npysort_sources) + npymath_sources)
    multiarray_src = [join('src', 'multiarray', 'alloc.c'), join('src', 'multiarray', 'arrayobject.c'), join('src', 'multiarray', 'arraytypes.c.src'), join('src', 'multiarray', 'array_assign_scalar.c'), join('src', 'multiarray', 'array_assign_array.c'), join('src', 'multiarray', 'arrayfunction_override.c'), join('src', 'multiarray', 'buffer.c'), join('src', 'multiarray', 'calculation.c'), join('src', 'multiarray', 'compiled_base.c'), join('src', 'multiarray', 'common.c'), join('src', 'multiarray', 'convert.c'), join('src', 'multiarray', 'convert_datatype.c'), join('src', 'multiarray', 'conversion_utils.c'), join('src', 'multiarray', 'ctors.c'), join('src', 'multiarray', 'datetime.c'), join('src', 'multiarray', 'datetime_strings.c'), join('src', 'multiarray', 'datetime_busday.c'), join('src', 'multiarray', 'datetime_busdaycal.c'), join('src', 'multiarray', 'descriptor.c'), join('src', 'multiarray', 'dragon4.c'), join('src', 'multiarray', 'dtype_transfer.c'), join('src', 'multiarray', 'einsum.c.src'), join('src', 'multiarray', 'flagsobject.c'), join('src', 'multiarray', 'getset.c'), join('src', 'multiarray', 'hashdescr.c'), join('src', 'multiarray', 'item_selection.c'), join('src', 'multiarray', 'iterators.c'), join('src', 'multiarray', 'lowlevel_strided_loops.c.src'), join('src', 'multiarray', 'mapping.c'), join('src', 'multiarray', 'methods.c'), join('src', 'multiarray', 'multiarraymodule.c'), join('src', 'multiarray', 'nditer_templ.c.src'), join('src', 'multiarray', 'nditer_api.c'), join('src', 'multiarray', 'nditer_constr.c'), join('src', 'multiarray', 'nditer_pywrap.c'), join('src', 'multiarray', 'number.c'), join('src', 'multiarray', 'refcount.c'), join('src', 'multiarray', 'sequence.c'), join('src', 'multiarray', 'shape.c'), join('src', 'multiarray', 'scalarapi.c'), join('src', 'multiarray', 'scalartypes.c.src'), join('src', 'multiarray', 'strfuncs.c'), join('src', 'multiarray', 'temp_elide.c'), join('src', 'multiarray', 'typeinfo.c'), join('src', 'multiarray', 'usertypes.c'), join('src', 'multiarray', 'vdot.c')]

    def generate_umath_c(ext, build_dir):
        target = join(build_dir, header_dir, '__umath_generated.c')
        dir = os.path.dirname(target)
        if (not os.path.exists(dir)):
            os.makedirs(dir)
        script = generate_umath_py
        if newer(script, target):
            f = open(target, 'w')
            f.write(generate_umath.make_code(generate_umath.defdict, generate_umath.__file__))
            f.close()
        return []
    umath_src = [join('src', 'umath', 'umathmodule.c'), join('src', 'umath', 'reduction.c'), join('src', 'umath', 'funcs.inc.src'), join('src', 'umath', 'simd.inc.src'), join('src', 'umath', 'loops.h.src'), join('src', 'umath', 'loops.c.src'), join('src', 'umath', 'matmul.h.src'), join('src', 'umath', 'matmul.c.src'), join('src', 'umath', 'clip.h.src'), join('src', 'umath', 'clip.c.src'), join('src', 'umath', 'ufunc_object.c'), join('src', 'umath', 'extobj.c'), join('src', 'umath', 'cpuid.c'), join('src', 'umath', 'scalarmath.c.src'), join('src', 'umath', 'ufunc_type_resolution.c'), join('src', 'umath', 'override.c')]
    umath_deps = [generate_umath_py, join('include', 'numpy', 'npy_math.h'), join('include', 'numpy', 'halffloat.h'), join('src', 'multiarray', 'common.h'), join('src', 'multiarray', 'number.h'), join('src', 'common', 'templ_common.h.src'), join('src', 'umath', 'simd.inc.src'), join('src', 'umath', 'override.h'), join(codegen_dir, 'generate_ufunc_api.py')]
    config.add_extension('_multiarray_umath', sources=((((multiarray_src + umath_src) + npymath_sources) + common_src) + [generate_config_h, generate_numpyconfig_h, generate_numpy_api, join(codegen_dir, 'generate_numpy_api.py'), join('*.py'), generate_umath_c, generate_ufunc_api]), depends=(((deps + multiarray_deps) + umath_deps) + common_deps), libraries=['npymath', 'npysort'], extra_info=extra_info)
    config.add_extension('_umath_tests', sources=[join('src', 'umath', '_umath_tests.c.src')])
    config.add_extension('_rational_tests', sources=[join('src', 'umath', '_rational_tests.c.src')])
    config.add_extension('_struct_ufunc_tests', sources=[join('src', 'umath', '_struct_ufunc_tests.c.src')])
    config.add_extension('_operand_flag_tests', sources=[join('src', 'umath', '_operand_flag_tests.c.src')])
    config.add_data_dir('tests')
    config.add_data_dir('tests/data')
    config.make_svn_version_py()
    return config