

def get_module_docs(self, path, contents):
    '\n        :type path: str\n        :type contents: str\n        :rtype: dict[str, any]\n        '
    module_doc_types = ['DOCUMENTATION', 'EXAMPLES', 'RETURN']
    docs = {
        
    }

    def check_assignment(statement, doc_types=None):
        'Check the given statement for a documentation assignment.'
        for target in statement.targets:
            if isinstance(target, ast.Tuple):
                continue
            if (doc_types and (target.id not in doc_types)):
                continue
            docs[target.id] = dict(yaml=statement.value.s, lineno=statement.lineno, end_lineno=(statement.lineno + len(statement.value.s.splitlines())))
    module_ast = self.parse_module(path, contents)
    if (not module_ast):
        return {
            
        }
    if path.startswith('lib/ansible/modules/'):
        for body_statement in module_ast.body:
            if isinstance(body_statement, ast.Assign):
                check_assignment(body_statement, module_doc_types)
    elif path.startswith('lib/ansible/utils/module_docs_fragments/'):
        for body_statement in module_ast.body:
            if isinstance(body_statement, ast.ClassDef):
                for class_statement in body_statement.body:
                    if isinstance(class_statement, ast.Assign):
                        check_assignment(class_statement)
    else:
        raise Exception(('unsupported path: %s' % path))
    return docs
