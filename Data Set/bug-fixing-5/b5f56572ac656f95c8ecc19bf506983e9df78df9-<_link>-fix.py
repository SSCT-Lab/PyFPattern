def _link(self, body, headers, include_dirs, libraries, library_dirs, lang):
    if (self.compiler.compiler_type == 'msvc'):
        libraries = (libraries or [])[:]
        library_dirs = (library_dirs or [])[:]
        if (lang in ['f77', 'f90']):
            lang = 'c'
            if self.fcompiler:
                for d in (self.fcompiler.library_dirs or []):
                    if d.startswith('/usr/lib'):
                        try:
                            d = subprocess.check_output(['cygpath', '-w', d])
                        except (OSError, subprocess.CalledProcessError):
                            pass
                        else:
                            d = filepath_from_subprocess_output(d)
                    library_dirs.append(d)
                for libname in (self.fcompiler.libraries or []):
                    if (libname not in libraries):
                        libraries.append(libname)
        for libname in libraries:
            if libname.startswith('msvc'):
                continue
            fileexists = False
            for libdir in (library_dirs or []):
                libfile = os.path.join(libdir, ('%s.lib' % libname))
                if os.path.isfile(libfile):
                    fileexists = True
                    break
            if fileexists:
                continue
            fileexists = False
            for libdir in library_dirs:
                libfile = os.path.join(libdir, ('lib%s.a' % libname))
                if os.path.isfile(libfile):
                    libfile2 = os.path.join(libdir, ('%s.lib' % libname))
                    copy_file(libfile, libfile2)
                    self.temp_files.append(libfile2)
                    fileexists = True
                    break
            if fileexists:
                continue
            log.warn(('could not find library %r in directories %s' % (libname, library_dirs)))
    elif (self.compiler.compiler_type == 'mingw32'):
        generate_manifest(self)
    return self._wrap_method(old_config._link, lang, (body, headers, include_dirs, libraries, library_dirs, lang))