def build_extension(self, ext):
    if self.__is_using_gnu_linker(ext):
        export_symbols = self.get_export_symbols(ext)
        text = ('{global: %s; local: *; };' % (';'.join(export_symbols),))
        script_fn = os.path.join(self.build_temp, 'link-version-{}.map'.format(ext.name))
        with open(script_fn, 'w') as f:
            f.write(text)
            ext.extra_link_args = [arg for arg in ext.extra_link_args if (not ('version-script' in arg))]
            ext.extra_link_args.append(('-Wl,--version-script=' + script_fn))
    old_build_ext.build_extension(self, ext)