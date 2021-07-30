import ast
from pprint import pprint

import astunparse


def get_deps(code):
    body = ast.parse(code)
    _, statements = next(ast.iter_fields(body))

    if isinstance(statements[0], ast.FunctionDef):
        statements = statements[0].body

    # Line no. at which each identifier was first seen
    declaration_line_num_map = {}
    ddg = {}

    def update_decls(lhs_vars_input, num):
        lhs_var_nodes = []
        for var_node in lhs_vars_input:
            lhs_var_nodes.append(var_node)
            if isinstance(var_node, ast.Attribute):
                # if var_node.attr not in declaration_line_num_map:

                if isinstance(var_node.value, ast.Attribute):
                    declaration_line_num_map[
                        var_node.value.value.id + '.' + var_node.value.attr + '.' + var_node.attr] = num
                    ddg[var_node.value.value.id + '.' + var_node.value.attr + '.' + var_node.attr] = set()
                else:
                    declaration_line_num_map[var_node.value.id + '.' + var_node.attr] = num
                    ddg[var_node.value.id + '.' + var_node.attr] = set()

            if isinstance(var_node, ast.Tuple) or isinstance(var_node, ast.List):
                for sub_var_node in var_node.elts:
                    if isinstance(sub_var_node, ast.Name):
                        if sub_var_node.id not in declaration_line_num_map:
                            declaration_line_num_map[sub_var_node.id] = num
                            ddg[sub_var_node.id] = set()
            elif isinstance(var_node, (ast.Subscript, ast.Attribute)):

                if isinstance(var_node.value, ast.Name):
                    if var_node.value.id not in declaration_line_num_map:
                        declaration_line_num_map[var_node.value.id] = num
                        ddg[var_node.value.id] = set()

                elif isinstance(var_node.value, ast.Attribute):

                    if isinstance(var_node.value.value, ast.Attribute):
                        # if var_node.value.value.attr not in declaration_line_num_map:
                        declaration_line_num_map[
                            var_node.value.value.value.id + '.' + var_node.value.value.attr + '.' + var_node.value.attr] = num

                        # print(var_node.value.value.value.id + '.' + var_node.value.value.attr + '.' + var_node.value.attr)
                        ddg[
                            var_node.value.value.value.id + '.' + var_node.value.value.attr + '.' + var_node.value.attr] = set()

                    if isinstance(var_node.value.value, ast.Name):
                        if hasattr(var_node, 'attr'):
                            declaration_line_num_map[
                                var_node.value.value.id + '.' + var_node.value.attr + '.' + var_node.attr] = num
                            # print(var_node.value.value.id + '.' + var_node.value.attr + '.' + var_node.attr)
                            ddg[var_node.value.value.id + '.' + var_node.value.attr + '.' + var_node.attr] = set()
                        else:
                            declaration_line_num_map[var_node.value.value.id + '.' + var_node.value.attr] = num
                            # print(var_node.value.value.id + '.' + var_node.value.attr)
                            ddg[var_node.value.value.id + '.' + var_node.value.attr] = set()

            else:
                if var_node.id not in declaration_line_num_map:
                    declaration_line_num_map[var_node.id] = num
                    ddg[var_node.id] = set()

        # pprint(ddg)
        # print()
        return lhs_var_nodes

    # x1, x2, x3, ..., xN = 1, 2, 3, 4, 5, ..., N
    # is represented in the AST as:
    #   - R = ast.Assign is root
    #   - R.targets gives the LHS
    #   - R.values

    def createNameMap(a, d=None):
        if type(a) == ast.Assign:
            # if isinstance(node, ast.Assign):
            identifier_names = a.targets
            lhs_vars = update_decls(identifier_names, seq_no)

            self_edge_occurrences_to_ignore = {x: 1 for x in identifier_names}

            # DFS in RHS
            depends_on = []
            for descendant in ast.walk(a):
                if descendant in self_edge_occurrences_to_ignore and self_edge_occurrences_to_ignore[descendant] > 0:
                    self_edge_occurrences_to_ignore[descendant] -= 1
                    continue
                if isinstance(descendant, ast.Name):
                    depends_on.append(descendant)

                if isinstance(descendant, ast.Attribute):
                    depends_on.append(descendant)

            for var in lhs_vars:
                for dependency in depends_on:

                    # if isinstance(var, ast.Attribute):
                    #
                    #     if isinstance(dependency, ast.Attribute):
                    #         if isinstance(var.value, ast.Attribute):
                    #             if isinstance(var.value.value, ast.Attribute):
                    #                     ddg[var.value.value.value.id + '.' + var.value.value.attr + '.' + var.value.attr].add(
                    #                         dependency.value.id + '.' + dependency.attr)
                    #             else:
                    #                 ddg[var.value.value.id + '.' + var.value.attr].add(
                    #                 dependency.value.id + '.' + dependency.attr)
                    #
                    #         elif isinstance(var.value, ast.Name):
                    #                 ddg[var.value.id].add(dependency.value.id + '.' + dependency.attr)
                    #
                    #     if isinstance(dependency, ast.Name):
                    #         if isinstance(var.value, ast.Attribute):
                    #             ddg[var.value.value.id + '.' + var.value.attr + '.' + var.attr].add(dependency.id)
                    #         else:
                    #             ddg[var.value.id + '.' + var.attr].add(dependency.id)

                    if isinstance(var, ast.Tuple) or isinstance(var, ast.List):
                        for sub_var in var.elts:
                            if isinstance(dependency, ast.Attribute):
                                if isinstance(dependency.value, ast.Name):
                                    if isinstance(sub_var, ast.Name):
                                        ddg[sub_var.id].add(dependency.value.id + '.' + dependency.attr)
                            else:
                                if isinstance(sub_var, ast.Name):
                                    ddg[sub_var.id].add(dependency.id)
                    elif isinstance(var, (ast.Subscript, ast.Attribute)):

                        if isinstance(dependency, ast.Attribute):
                            if isinstance(dependency.value, ast.Name):
                                if isinstance(var.value, ast.Attribute):
                                    if isinstance(var.value.value, ast.Attribute):
                                        ddg[
                                            var.value.value.value.id + '.' + var.value.value.attr + '.' + var.value.attr].add(
                                            dependency.value.id + '.' + dependency.attr)
                                    else:
                                        ddg[var.value.value.id + '.' + var.value.attr].add(
                                            dependency.value.id + '.' + dependency.attr)
                                elif isinstance(var.value, ast.Name):
                                    ddg[var.value.id].add(dependency.value.id + '.' + dependency.attr)

                            elif isinstance(dependency.value, ast.Attribute):
                                if isinstance(var.value, ast.Attribute):
                                    if isinstance(var.value.value, ast.Attribute):

                                        if isinstance(dependency.value.value, ast.Attribute):
                                            ddg[
                                                var.value.value.value.id + '.' + var.value.value.attr + '.' + var.value.attr].add(
                                                dependency.value.value.id + '.' + dependency.value.attr + '.' + dependency.attr)
                                        else:
                                            ddg[
                                                var.value.value.value.id + '.' + var.value.value.attr + '.' + var.value.attr].add(
                                                dependency.value.value.id + '.' + dependency.value.attr + '.' + dependency.attr)


                                    else:
                                        if hasattr(var, 'attr'):
                                            ddg[var.value.value.id + '.' + var.value.attr + '.' + var.attr].add(
                                                dependency.value.value.id + '.' + dependency.value.attr + '.' + dependency.attr)
                                        else:
                                            ddg[var.value.value.id + '.' + var.value.attr].add(
                                                dependency.value.value.id + '.' + dependency.value.attr)

                                elif isinstance(var.value, ast.Name):

                                    if hasattr(var, 'attr'):
                                        ddg[var.value.id + '.' + var.attr].add(
                                            dependency.value.value.id + '.' + dependency.value.attr + '.' + dependency.attr)
                                    else:
                                        ddg[var.value.id].add(
                                            dependency.value.value.id + '.' + dependency.value.attr + '.' + dependency.attr)

                        if isinstance(dependency, ast.Name):
                            if isinstance(var.value, ast.Name):
                                ddg[var.value.id].add(dependency.id)
                            elif isinstance(var.value, ast.Attribute):
                                if isinstance(var.value.value, ast.Attribute):
                                    s = str(
                                        var.value.value.value.id + '.' + var.value.value.attr + '.' + var.value.attr)
                                    if s not in ddg: print(s, dependency.id)
                                    ddg[s].add(dependency.id)
                                else:
                                    ddg[var.value.value.id + '.' + var.value.attr].add(dependency.id)

                    else:
                        if isinstance(dependency, ast.Attribute):

                            if isinstance(dependency.value, ast.Name):
                                ddg[var.id].add(dependency.value.id + '.' + dependency.attr)

                        else:
                            ddg[var.id].add(dependency.id)

        for child in ast.iter_child_nodes(a):
            createNameMap(child, d)

    for seq_no, node in enumerate(statements):
        createNameMap(node)

    # for seq_no, node in enumerate(statements):
    #
    #     if isinstance(node, ast.Assign):
    #         identifier_names = node.targets
    #         lhs_vars = update_decls(identifier_names, seq_no)
    #
    #         self_edge_occurrences_to_ignore = {x: 1 for x in identifier_names}
    #
    #         # DFS in RHS
    #         depends_on = []
    #         for descendant in ast.walk(node):
    #             if descendant in self_edge_occurrences_to_ignore and self_edge_occurrences_to_ignore[descendant] > 0:
    #                 self_edge_occurrences_to_ignore[descendant] -= 1
    #                 continue
    #             if isinstance(descendant, ast.Name):
    #                 depends_on.append(descendant)
    #
    #             if isinstance(descendant, ast.Attribute):
    #                 depends_on.append(descendant)
    #
    #         for var in lhs_vars:
    #             for dependency in depends_on:
    #                 if isinstance(var, ast.Attribute):
    #                     if isinstance(dependency, ast.Attribute):
    #                         if isinstance(var.value, ast.Attribute):
    #                             ddg[var.value.value.id + '.' + var.value.attr + '.' + var.attr].add(
    #                                 dependency.value.id + '.' + dependency.attr)
    #                         else:
    #
    #                             if isinstance(dependency.value, ast.Attribute):
    #
    #                                 ddg[var.value.id + '.' + var.attr].add(
    #                                     dependency.value.value.id + '.' + dependency.value.attr + '.' + dependency.attr)
    #                             else:
    #                                 ddg[var.value.id + '.' + var.attr].add(
    #                                     dependency.value.id + '.' + dependency.attr)
    #                     else:
    #                         if isinstance(var.value, ast.Attribute):
    #                             ddg[var.value.value.id + '.' + var.value.attr + '.' + var.attr].add(dependency.id)
    #                         else:
    #                             ddg[var.value.id + '.' + var.attr].add(dependency.id)
    #
    #                 elif isinstance(var, ast.Tuple) or isinstance(var, ast.List):
    #                     for sub_var in var.elts:
    #                         if isinstance(dependency, ast.Attribute):
    #                             if isinstance(dependency.value, ast.Name):
    #                                 if isinstance(sub_var, ast.Name):
    #                                     ddg[sub_var.id].add(dependency.value.id + '.' + dependency.attr)
    #                         else:
    #                             if isinstance(sub_var, ast.Name):
    #                                 ddg[sub_var.id].add(dependency.id)
    #                 elif isinstance(var, ast.Subscript):
    #
    #                     if isinstance(dependency, ast.Attribute):
    #                         if isinstance(dependency.value, ast.Name):
    #                             if isinstance(var.value, ast.Attribute):
    #                                 if isinstance(var.value.value, ast.Attribute):
    #                                     ddg[var.value.value.value.id + '.' + var.value.value.attr + '.' + var.value.attr].add(
    #                                         dependency.value.id + '.' + dependency.attr)
    #                                 else:
    #                                     ddg[var.value.value.id + '.' + var.value.attr].add(
    #                                     dependency.value.id + '.' + dependency.attr)
    #                             elif isinstance(var.value, ast.Name):
    #                                 ddg[var.value.id].add(dependency.value.id + '.' + dependency.attr)
    #
    #                     if isinstance(dependency, ast.Name):
    #                         if isinstance(var.value, ast.Name):
    #                             ddg[var.value.id].add(dependency.id)
    #                         elif isinstance(var.value, ast.Attribute):
    #                             if isinstance(var.value.value, ast.Attribute):
    #                                 s = str(var.value.value.value.id + '.' + var.value.value.attr + '.' + var.value.attr)
    #                                 if s not in ddg : print(s,dependency.id)
    #                                 ddg[s].add(dependency.id)
    #                             else:
    #                                 ddg[var.value.value.id + '.' + var.value.attr].add(dependency.id)
    #
    #                 else:
    #                     if isinstance(dependency, ast.Attribute):
    #
    #                         if isinstance(dependency.value, ast.Name):
    #                             ddg[var.id].add(dependency.value.id + '.' + dependency.attr)
    #
    #                     else:
    #                         ddg[var.id].add(dependency.id)

    return declaration_line_num_map, ddg


class MethodLevelDDGs:
    def __init__(self, code):
        self.parsed_ast = ast.parse(code)

    def get_methods(self):
        fn_nodes = []

        class FnVisitor(ast.NodeVisitor):
            def visit_FunctionDef(self, node):
                fn_nodes.append(node)

        visitor = FnVisitor()
        visitor.visit(self.parsed_ast)
        return fn_nodes

    def recursive_ddg(self, fn_root_node):
        # print(astunparse.unparse(fn_root_node))

        s = astunparse.unparse(fn_root_node)
        declaration_line_num_map, ddg = get_deps(s)
        # pprint(declaration_line_num_map)

        return declaration_line_num_map, ddg

        ## archiving
        # ddg = {}
        # self_edge_set = set()

        # class DDGVisitor(ast.NodeVisitor):
        #     def visit_Assign(self, node):
        #         identifiers = node.targets
        #
        #         for identifier in identifiers:
        #
        #             if isinstance(identifier, ast.Name):
        #                 ddg[identifier.id] = set()
        #                 self_edge_set.add(identifier.id)
        #
        #             if isinstance(identifier, ast.Attribute):
        #                 ddg[identifier.attr] = set()
        #                 self_edge_set.add(identifier.attr)
        #
        #                 # ddg[identifier.value.id+'.'+identifier.attr] = set()
        #                 # self_edge_set.add(identifier.value.id+'.'+identifier.attr)
        #
        #
        #         depends_on = []
        #         for descendant in ast.walk(node):
        #             if isinstance(descendant, ast.Name):
        #                 depends_on.append(descendant)
        #
        #         for var in identifiers:
        #             for dependency in depends_on:
        #
        #                 if isinstance(var, ast.Name):
        #                     if var.id in self_edge_set:
        #                         self_edge_set.remove(var.id)
        #                         continue
        #                     ddg[var.id].add(dependency.id)
        #
        #                 if isinstance(var, ast.Attribute):
        #                     if var.attr in self_edge_set:
        #                         self_edge_set.remove(var.attr)
        #                         # self_edge_set.remove(var.value.id+'.'+var.attr)
        #                         continue
        #                     ddg[var.attr].add(dependency.id)
        #                     # ddg[var.value.id+'.'+var.attr].add(dependency.id)
        #
        # visitor = DDGVisitor()
        # visitor.visit(fn_root_node)
        # return ddg


def fn_ddgs(code):
    method_level_ddgs = MethodLevelDDGs(code)
    methods = method_level_ddgs.get_methods()
    # ddgs = {method.name: method_level_ddgs.recursive_ddg(method) for method in methods}
    declaration_line_num_maps = {}
    ddgs = {}
    for method in methods:
        declaration_line_num_map, ddg = method_level_ddgs.recursive_ddg(method)
        declaration_line_num_maps[method.name] = declaration_line_num_map
        ddgs[method.name] = ddg

    return declaration_line_num_maps, ddgs
