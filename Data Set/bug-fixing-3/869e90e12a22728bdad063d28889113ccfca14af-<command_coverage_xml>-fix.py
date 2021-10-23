def command_coverage_xml(args):
    '\n    :type args: CoverageConfig\n    '
    output_files = command_coverage_combine(args)
    for output_file in output_files:
        xml_name = ('test/results/reports/%s.xml' % os.path.basename(output_file))
        env = common_environment()
        env.update(dict(COVERAGE_FILE=output_file))
        run_command(args, env=env, cmd=['coverage', 'xml', '-i', '-o', xml_name])