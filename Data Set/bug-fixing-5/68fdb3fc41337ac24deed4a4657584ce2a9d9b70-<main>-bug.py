def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
    docs_dir = os.path.join(base_dir, 'docs')
    schemas = defs.get_all_schemas()
    ml = is_ml(schemas)
    if ml:
        fname = os.path.join(docs_dir, 'TestCoverage-ml.md')
    else:
        fname = os.path.join(docs_dir, 'TestCoverage.md')
    with open(fname, 'w+') as f:
        gen_outlines(f, ml)
        gen_node_test_coverage(schemas, f, ml)
        gen_model_test_coverage(schemas, f, ml)
        gen_overall_test_coverage(schemas, f, ml)