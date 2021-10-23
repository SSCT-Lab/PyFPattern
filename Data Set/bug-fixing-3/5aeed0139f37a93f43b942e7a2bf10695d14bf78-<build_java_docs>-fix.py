def build_java_docs(app):
    'build java docs and then move the outdir'
    java_path = (app.builder.srcdir + '/../scala-package')
    java_doc_sources = 'find . -type f -name "*.scala" | egrep "\\.\\/core|\\.\\/infer" | egrep "\\/javaapi" | egrep -v "Suite"'
    java_doc_classpath = ':'.join(['`find native -name "*.jar" | grep "target/lib/" | tr "\\n" ":" `', '`find macros -name "*.jar" | tr "\\n" ":" `', '`find core -name "*.jar" | tr "\\n" ":" `', '`find infer -name "*.jar" | tr "\\n" ":" `'])
    _run_cmd('cd {}; scaladoc `{}` -classpath {} -feature -deprecation'.format(java_path, java_doc_sources, java_doc_classpath))
    dest_path = (app.builder.outdir + '/api/java/docs')
    _run_cmd(('rm -rf ' + dest_path))
    _run_cmd(('mkdir -p ' + dest_path))
    javadocs = ['index', 'index.html', 'org', 'lib', 'index.js', 'package.html']
    for doc_file in javadocs:
        _run_cmd((((((('cd ' + java_path) + ' && mv -f ') + doc_file) + ' ') + dest_path) + '; exit 0'))