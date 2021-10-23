

def write_data(text, output_dir, outputname, module=None):
    ' dumps module output to a file or the screen, as requested '
    if (output_dir is not None):
        if module:
            outputname = (outputname % module)
        if (not os.path.exists(output_dir)):
            os.makedirs(output_dir)
        fname = os.path.join(output_dir, outputname)
        fname = fname.replace('.py', '')
        with open(fname, 'wb') as f:
            f.write(to_bytes(text))
    else:
        print(text)
