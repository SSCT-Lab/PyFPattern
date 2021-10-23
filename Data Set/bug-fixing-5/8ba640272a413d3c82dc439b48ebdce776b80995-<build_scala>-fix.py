def build_scala(app):
    'build scala for scala docs, java docs, and clojure docs to use'
    if any(((v in _BUILD_VER) for v in ['1.2.', '1.3.', '1.4.'])):
        _run_cmd(('cd %s/.. && make scalapkg' % app.builder.srcdir))
        _run_cmd(('cd %s/.. && make scalainstall' % app.builder.srcdir))
    else:
        _run_cmd(('cd %s/../scala-package && mvn -B install -DskipTests' % app.builder.srcdir))