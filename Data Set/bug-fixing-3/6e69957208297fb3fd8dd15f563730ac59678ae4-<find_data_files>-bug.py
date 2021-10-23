def find_data_files():
    "\n    Find IPython's data_files.\n\n    Just man pages at this point.\n    "
    manpagebase = pjoin('share', 'man', 'man1')
    manpages = [f for f in glob(pjoin('docs', 'man', '*.1.gz')) if isfile(f)]
    if (not manpages):
        manpages = [f for f in glob(pjoin('docs', 'man', '*.1')) if isfile(f)]
    data_files = [(manpagebase, manpages)]
    return data_files