def lint(self, fragment):
    'Lint a ChangelogFragment.\n        :type fragment: ChangelogFragment\n        :rtype: list[(str, int, int, str)]\n        '
    errors = []
    for (section, lines) in fragment.content.items():
        if (section not in self.config.sections):
            errors.append((fragment.path, 0, 0, ('invalid section: %s' % section)))
        if isinstance(lines, list):
            for line in lines:
                results = rstcheck.check(line, filename=fragment.path, report_level=docutils.utils.Reporter.WARNING_LEVEL)
                errors += [(fragment.path, 0, 0, result[1]) for result in results]
        else:
            results = rstcheck.check(lines, filename=fragment.path, report_level=docutils.utils.Reporter.WARNING_LEVEL)
            errors += [(fragment.path, 0, 0, result[1]) for result in results]
    return errors