

def build_scala_docs(app):
    'build scala doc and then move the outdir'
    scala_path = (app.builder.srcdir + '/../scala-package')
    scala_doc_sources = 'find . -type f -name "*.scala" | egrep "\\.\\/core|\\.\\/infer" | egrep -v "Suite"'
    scala_doc_classpath = ':'.join(['`find native -name "*.jar" | grep "target/lib/" | tr "\\n" ":" `', '`find macros -name "*-SNAPSHOT.jar" | tr "\\n" ":" `'])
    _run_cmd('cd {}; scaladoc `{}` -classpath {} -feature -deprecation; exit 0'.format(scala_path, scala_doc_sources, scala_doc_classpath))
    dest_path = (app.builder.outdir + '/api/scala/docs')
    _run_cmd(('rm -rf ' + dest_path))
    _run_cmd(('mkdir -p ' + dest_path))
    scaladocs = ['index', 'index.html', 'org', 'lib', 'index.js', 'package.html']
    for doc_file in scaladocs:
        _run_cmd((((((('cd ' + scala_path) + ' && mv -f ') + doc_file) + ' ') + dest_path) + '; exit 0'))
