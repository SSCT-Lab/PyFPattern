def get_build_ext_override():
    '\n    Custom build_ext command to tweak extension building.\n    '
    from numpy.distutils.command.build_ext import build_ext as old_build_ext

    class build_ext(old_build_ext):

        def build_extension(self, ext):
            if self.__is_using_gnu_linker(ext):
                export_symbols = self.get_export_symbols(ext)
                text = ('{global: %s; local: *; };' % (';'.join(export_symbols),))
                script_fn = os.path.join(self.build_temp, 'link-version-{}.map'.format(ext.name))
                with open(script_fn, 'w') as f:
                    f.write(text)
                    ext.extra_link_args.append(('-Wl,--version-script=' + script_fn))
            old_build_ext.build_extension(self, ext)

        def __is_using_gnu_linker(self, ext):
            if (not sys.platform.startswith('linux')):
                return False
            if (ext.language == 'f90'):
                is_gcc = (self._f90_compiler.compiler_type in ('gnu', 'gnu95'))
            elif (ext.language == 'f77'):
                is_gcc = (self._f77_compiler.compiler_type in ('gnu', 'gnu95'))
            else:
                is_gcc = False
                if (self.compiler.compiler_type == 'unix'):
                    cc = sysconfig.get_config_var('CC')
                    if (not cc):
                        cc = ''
                    compiler_name = os.path.basename(cc)
                    is_gcc = (('gcc' in compiler_name) or ('g++' in compiler_name))
            return (is_gcc and (sysconfig.get_config_var('GNULD') == 'yes'))
    return build_ext