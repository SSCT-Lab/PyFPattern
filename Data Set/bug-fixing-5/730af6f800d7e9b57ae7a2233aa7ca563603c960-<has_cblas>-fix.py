def has_cblas(self, info):
    res = False
    c = distutils.ccompiler.new_compiler()
    c.customize('')
    tmpdir = tempfile.mkdtemp()
    s = '#include <cblas.h>\n        int main(int argc, const char *argv[])\n        {\n            double a[4] = {1,2,3,4};\n            double b[4] = {5,6,7,8};\n            return cblas_ddot(4, a, 1, b, 1) > 10;\n        }'
    src = os.path.join(tmpdir, 'source.c')
    try:
        with open(src, 'wt') as f:
            f.write(s)
        try:
            obj = c.compile([src], output_dir=tmpdir, include_dirs=self.get_include_dirs())
            try:
                c.link_executable(obj, os.path.join(tmpdir, 'a.out'), libraries=['cblas'], library_dirs=info['library_dirs'], extra_postargs=info.get('extra_link_args', []))
                res = 'cblas'
            except distutils.ccompiler.LinkError:
                c.link_executable(obj, os.path.join(tmpdir, 'a.out'), libraries=['blas'], library_dirs=info['library_dirs'], extra_postargs=info.get('extra_link_args', []))
                res = 'blas'
        except distutils.ccompiler.CompileError:
            res = None
    finally:
        shutil.rmtree(tmpdir)
    return res