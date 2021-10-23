

def _check_conditional(self, conditional, templar, all_vars):
    '\n        This method does the low-level evaluation of each conditional\n        set on this object, using jinja2 to wrap the conditionals for\n        evaluation.\n        '
    original = conditional
    if ((conditional is None) or (conditional == '')):
        return True
    if isinstance(conditional, bool):
        return conditional
    if templar.is_template(conditional):
        display.warning(('conditional statements should not include jinja2 templating delimiters such as {{ }} or {%% %%}. Found: %s' % conditional))
    bare_vars_warning = False
    if C.CONDITIONAL_BARE_VARS:
        if ((conditional in all_vars) and VALID_VAR_REGEX.match(conditional)):
            conditional = all_vars[conditional]
            bare_vars_warning = True
    templar.available_variables = all_vars
    try:
        disable_lookups = hasattr(conditional, '__UNSAFE__')
        conditional = templar.template(conditional, disable_lookups=disable_lookups)
        if (bare_vars_warning and (not isinstance(conditional, bool))):
            display.deprecated(('evaluating %s as a bare variable, this behaviour will go away and you might need to add |bool to the expression in the future. Also see CONDITIONAL_BARE_VARS configuration toggle.' % conditional), '2.12')
        if ((not isinstance(conditional, text_type)) or (conditional == '')):
            return conditional
        disable_lookups |= hasattr(conditional, '__UNSAFE__')

        class CleansingNodeVisitor(ast.NodeVisitor):

            def generic_visit(self, node, inside_call=False, inside_yield=False):
                if isinstance(node, ast.Call):
                    inside_call = True
                elif isinstance(node, ast.Yield):
                    inside_yield = True
                elif isinstance(node, ast.Str):
                    if disable_lookups:
                        if (inside_call and node.s.startswith('__')):
                            raise AnsibleError(("Invalid access found in the conditional: '%s'" % conditional))
                        elif inside_yield:
                            parsed = ast.parse(node.s, mode='exec')
                            cnv = CleansingNodeVisitor()
                            cnv.visit(parsed)
                for child_node in ast.iter_child_nodes(node):
                    self.generic_visit(child_node, inside_call=inside_call, inside_yield=inside_yield)
        try:
            e = templar.environment.overlay()
            e.filters.update(templar._get_filters())
            e.tests.update(templar._get_tests())
            res = e._parse(conditional, None, None)
            res = generate(res, e, None, None)
            parsed = ast.parse(res, mode='exec')
            cnv = CleansingNodeVisitor()
            cnv.visit(parsed)
        except Exception as e:
            raise AnsibleError(('Invalid conditional detected: %s' % to_native(e)))
        presented = ('{%% if %s %%} True {%% else %%} False {%% endif %%}' % conditional)
        val = templar.template(presented, disable_lookups=disable_lookups).strip()
        if (val == 'True'):
            return True
        elif (val == 'False'):
            return False
        else:
            raise AnsibleError(('unable to evaluate conditional: %s' % original))
    except (AnsibleUndefinedVariable, UndefinedError) as e:
        try:
            var_name = re.compile("'(hostvars\\[.+\\]|[\\w_]+)' is undefined").search(str(e)).groups()[0]
            def_undef = self.extract_defined_undefined(conditional)
            for (du_var, logic, state) in def_undef:
                if (var_name.replace("'", '"') == du_var.replace("'", '"')):
                    should_exist = (('not' in logic) != (state == 'defined'))
                    if should_exist:
                        return False
                    else:
                        return True
            raise
        except Exception:
            raise AnsibleUndefinedVariable(('error while evaluating conditional (%s): %s' % (original, e)))
