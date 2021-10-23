def write_data(text, options, outputname, module):
    ' dumps module output to a file or the screen, as requested '
    if (options.output_dir is not None):
        fname = os.path.join(options.output_dir, (outputname % module))
        fname = fname.replace('.py', '')
        f = open(fname, 'w')
        f.write(text.encode('utf-8'))
        f.close()
    else:
        print(text)