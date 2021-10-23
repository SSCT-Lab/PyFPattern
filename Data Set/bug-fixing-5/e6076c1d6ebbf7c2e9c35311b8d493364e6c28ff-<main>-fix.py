def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
    docs_dir = os.path.join(base_dir, 'docs')
    schemas = defs.get_all_schemas()
    has_ml = is_ml(schemas)
    fname = os.path.join(docs_dir, 'TestCoverage.md')
    with io.open(fname, 'w+', newline='', encoding='utf-8') as f:
        gen_outlines(f, False)
        gen_node_test_coverage(schemas, f, False)
        gen_model_test_coverage(schemas, f, False)
        gen_overall_test_coverage(schemas, f, False)
    if has_ml:
        fname = os.path.join(docs_dir, 'TestCoverage-ml.md')
        with io.open(fname, 'w+', newline='', encoding='utf-8') as f:
            gen_outlines(f, True)
            gen_node_test_coverage(schemas, f, True)
            gen_model_test_coverage(schemas, f, True)
            gen_overall_test_coverage(schemas, f, True)