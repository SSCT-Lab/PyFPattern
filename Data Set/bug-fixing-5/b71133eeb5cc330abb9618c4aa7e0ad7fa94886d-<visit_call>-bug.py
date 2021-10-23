@check_messages(*MSGS.keys())
def visit_call(self, node):
    version = None
    try:
        if (((node.func.attrname == 'deprecated') and ('display' in _get_expr_name(node))) or ((node.func.attrname == 'deprecate') and ('module' in _get_expr_name(node)))):
            if node.keywords:
                for keyword in node.keywords:
                    if ((len(node.keywords) == 1) and (keyword.arg is None)):
                        return
                    elif (keyword.arg == 'version'):
                        if isinstance(keyword.value.value, astroid.Name):
                            return
                        version = keyword.value.value
            if (not version):
                try:
                    version = node.args[1].value
                except IndexError:
                    self.add_message('ansible-deprecated-no-version', node=node)
                    return
            try:
                if (ANSIBLE_VERSION >= StrictVersion(str(version))):
                    self.add_message('ansible-deprecated-version', node=node, args=(version,))
            except ValueError:
                self.add_message('ansible-invalid-deprecated-version', node=node, args=(version,))
    except AttributeError:
        pass