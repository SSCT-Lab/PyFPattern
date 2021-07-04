import ast


class ReWriteName(ast.NodeTransformer):

    def __init__(self):
        self.defList = []
        self.varList = []
        self.argList = []
        self.funList = []
        self.numList = []
        self.strList = []
        self.moduleList = []
        self.keywords = ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue',
                         'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import',
                         'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while',
                         'with', 'yield']
        self.featureList = ['isinstance', 'type', 'globals', 'locals', 'dir', '__dir__', 'isclass',
                            'ismethod', 'isfunction', 'getattr', '__getattribute__', 'hasattr',
                            'issubclass', 'super', 'vars', 'delattr', '__delattr__', 'setattr',
                            '__setattr__', 'property', 'reload', '__import__', 'input', 'eval',
                            'exec', 'compile', 'execfile']

    def generic_visit(self, node):

        if hasattr(node, 'module'):
            # print("module------", node.module)
            if node.module not in self.moduleList:
                self.moduleList.append(node.module)
            for index_module in range(0, len(self.moduleList)):
                if str(node.module) == str(self.moduleList[index_module]):
                    node.module = 'module' + str(index_module + 1)

        elif hasattr(node, 'name'):
            # print("方法头------", node.name)
            if node.name not in self.defList:
                self.defList.append(node.name)
            for index_def in range(0, len(self.defList)):
                if str(node.name) == str(self.defList[index_def]):
                    # node.name = 'FunctionName' + str(index_def + 1)
                    node.name = 'FunctionName'

        elif hasattr(node, 'arg'):
            # print("参数------", node.arg)
            if node.arg not in self.argList:
                self.argList.append(node.arg)
            for index_arg in range(0, len(self.argList)):
                if str(node.arg) == str(self.argList[index_arg]):
                    node.arg = 'arg' + str(index_arg + 1)

        elif hasattr(node, 'attr'):
            # print("方法名------",node.attr)
            if (node.attr in self.keywords) or (node.attr in self.featureList):
                node.attr = node.attr
            else:
                if (node.attr not in self.funList):
                    self.funList.append(node.attr)
                for index_fun in range(0, len(self.funList)):
                    if str(node.attr) == str(self.funList[index_fun]):
                        node.attr = 'Fun' + str(index_fun + 1)

        elif hasattr(node, 'id'):
            # print("成员变量------",node.id)
            if (node.id in self.keywords) or (node.id in self.featureList):
                node.id = node.id
            else:
                if (node.id not in self.varList):
                    self.varList.append(node.id)
                for index_var in range(0, len(self.varList)):
                    if str(node.id) == str(self.varList[index_var]):
                        node.id = 'var' + str(index_var + 1)

        elif hasattr(node, 'n'):
            # print("n------", node.n)
            if (node.n not in self.numList):
                self.numList.append(node.n)
            for index_num in range(0, len(self.numList)):
                if str(node.n) == str(self.numList[index_num]):
                    # node.n = 'num' + str(index_num + 1)
                    node.n = 'num'


        elif hasattr(node, 's'):
            # print("s------", node.s)
            if (node.s not in self.strList):
                self.strList.append(node.s)
            for index_str in range(0, len(self.strList)):
                if str(node.s) == str(self.strList[index_str]):
                    # node.s = 'str' + str(index_str + 1)
                    node.s = 's'


        # else:
        #     print(node._fields)

        ast.NodeTransformer.generic_visit(self, node)
        return node
