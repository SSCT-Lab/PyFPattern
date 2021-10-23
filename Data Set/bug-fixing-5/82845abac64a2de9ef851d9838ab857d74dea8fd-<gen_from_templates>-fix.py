def gen_from_templates(templates, top_path):
    'Generate cython files from a list of templates'
    from Cython import Tempita
    for template in templates:
        outfile = template.replace('.tp', '')
        if (not (os.path.exists(outfile) and (os.stat(template).st_mtime < os.stat(outfile).st_mtime))):
            with open(template, 'r') as f:
                tmpl = f.read()
            tmpl_ = Tempita.sub(tmpl)
            with open(outfile, 'w') as f:
                f.write(tmpl_)