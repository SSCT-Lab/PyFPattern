def lint(self, fragment):
    'Lint a ChangelogFragment.\n        :type fragment: ChangelogFragment\n        :rtype: list[(str, int, int, str)]\n        '
    errors = []
    for (section, lines) in fragment.content.items():
        if (section == self.config.prelude_name):
            if (not isinstance(lines, string_types)):
                errors.append((fragment.path, 0, 0, ('section "%s" must be type str not %s' % (section, type(lines).__name__))))
        else:
            if (not isinstance(lines, list)):
                errors.append((fragment.path, 0, 0, ('section "%s" must be type list not %s' % (section, type(lines).__name__))))
            if (section not in self.config.sections):
                errors.append((fragment.path, 0, 0, ('invalid section: %s' % section)))
        if isinstance(lines, list):
            for line in lines:
                if (not isinstance(line, string_types)):
                    errors.append((fragment.path, 0, 0, ('section "%s" list items must be type str not %s' % (section, type(line).__name__))))
                    continue
                results = rstcheck.check(line, filename=fragment.path, report_level=docutils.utils.Reporter.WARNING_LEVEL)
                errors += [(fragment.path, 0, 0, result[1]) for result in results]
        elif isinstance(lines, string_types):
            results = rstcheck.check(lines, filename=fragment.path, report_level=docutils.utils.Reporter.WARNING_LEVEL)
            errors += [(fragment.path, 0, 0, result[1]) for result in results]
    return errors