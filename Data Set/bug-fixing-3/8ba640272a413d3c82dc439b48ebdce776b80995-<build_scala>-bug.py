def build_scala(app):
    'build scala for scala docs, java docs, and clojure docs to use'
    _run_cmd(('cd %s/../scala-package && mvn -B install -DskipTests' % app.builder.srcdir))