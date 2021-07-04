#!/usr/bin/env python3

import ast
import os
import shutil
import sys
from functools import partial
from pprint import pprint
import astunparse

from lcs import lcslen
from pyff.ddg import readBuggyCode
from pyff.ddg import render
from pyff.ddg.test import compareGraph
from pyff.diffFile.fixPattern import fix_pattern
from pyff.diffFile.reWriteName import ReWriteName


addCode = ''
delCode = ''

delCodeDict = {}
addCodeDict = {}

bugRefactorCodeDict = {}
fixRefactorCodeDict = {}

def codeDiff(c, x, y, i, j, ):
    global addCode, delCode

    if i < 0 and j < 0:
        pass
        # return ""
    elif x[i] == y[j]:
        codeDiff(c, x, y, i - 1, j - 1)
    elif i < 0:
        codeDiff(c, x, y, i, j - 1)
        # addCode += "+ " + y[j]
        addCode += y[j]
    elif j < 0:
        codeDiff(c, x, y, i - 1, j)
        # delCode += "- " + x[i]
        delCode += x[i]
    elif c[i][j - 1] >= c[i - 1][j]:
        codeDiff(c, x, y, i, j - 1)
        # addCode += "+ " + y[j]
        addCode += y[j]
    elif c[i][j - 1] < c[i - 1][j]:
        codeDiff(c, x, y, i - 1, j)
        # delCode += "- " + x[i]
        delCode += x[i]

def diff(x, y):
    c = lcslen(x, y)
    codeDiff(c, x, y, len(x) - 1, len(y) - 1)

def getFileList(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.py':
                L.append(os.path.join(root, file))
    return L

def getLocalVar_rename(L):
    global addCode, delCode
    for i in range(0, len(L) - 1, 2):
        if L[i].endswith('bug.py'):
            buggy = L[i]
            fixed = L[i + 1]
        else:
            buggy = L[i + 1]
            fixed = L[i]


        buggyCodeAST = ast.parse(open(buggy, 'r').read()).body
        fixedCodeAST = ast.parse(open(fixed, 'r').read()).body
        visitor = ReWriteName()
        for node in buggyCodeAST:
            funNode = visitor.visit(node)
            buggyCode = astunparse.unparse(funNode).splitlines()

        for node in fixedCodeAST:
            funNode = visitor.visit(node)
            fixedCode = astunparse.unparse(funNode).splitlines()

        diff(buggyCode, fixedCode)


        if len(delCode.splitlines()) ==1:
            if ('if (\'s\' in' in addCode) :
                print(buggy)
                print(delCode)
                print('++++++')
                print(addCode)
                print()

        # if addCode != '' and delCode != '':
        #     try:
        #         delCodeAST = ast.parse(delCode.strip())
        #         addCodeAST = ast.parse(addCode.strip())
        #
        #         for i in delCodeAST.body:
        #             codeType = str(type(i)).split("\'")[1]
        #             bugVar1 = readBuggyCode.parseBuggyCode(delCode.strip())
        #             bugVar2 = readBuggyCode.parseBuggyCode(addCode.strip())
        #
        #             if bugVar1 != bugVar2 and len(bugVar1) != 0 and len(bugVar2) != 0:
        #
        #                 delCodeDict[buggy] = bugVar1
        #                 addCodeDict[fixed] = bugVar2
        #
        #                 # print(fixed)
        #                 # print(addCode.strip(),'\n')
        #                 # print(bugVar2)
        #
        #                 # print(delCode.strip()+'\n')
        #                 # print('\n')
        #                 # print(addCode.strip()+'\n')
        #                 #
        #                 # f.write('##############################'+buggy+'##############################'+'\n')
        #                 # f.write(delCode.strip()+'\n')
        #                 # f.write('\n')
        #                 # f.write(addCode.strip()+'\n')
        #     except:
        #         pass

        addCode = ''
        delCode = ''
    # f.close()

def readCode(code): # AST syntax rule
    if len(code.splitlines()) == 1:
        code = code.splitlines()[0].strip()
        if code.startswith('if') or code.startswith('for') or code.startswith('with') or code.startswith('while'):
            code = code + 'pass'
    else:
        tag = 0
        for index in range(0,len(code)):
            if code[index] != ' ':
                tag = index
                break
        temp = ''
        for i in code.splitlines():
            temp = temp + i[tag:] + '\n'
        code = temp.strip()
    return code

def getLocalVar(L):
    global addCode, delCode

    for i in range(0, len(L) - 1, 2):
        if L[i].endswith('bug.py'):
            buggyPath = L[i]
            fixedPath = L[i + 1]
        else:
            buggyPath = L[i + 1]
            fixedPath = L[i]

        with open(buggyPath, 'r') as f1, open(fixedPath, 'r') as f2:
            try:
                bugcode = f1.readlines()
                fixcode = f2.readlines()
                diff(bugcode, fixcode)
            except:
                pass
                # print(buggy)

        delCode = readCode(delCode)
        addCode = readCode(addCode)

        if delCode == '' or delCode == '\n' or delCode == '\n\n': continue #print(buggyPath)  # bug code is null

        code_decls, ddg_graph = readBuggyCode.parseBuggyFile(buggyPath)
        fix_pattern(delCode,addCode,ddg_graph,buggyPath)

        addCode = ''
        delCode = ''

def ddgRefactor():
    pprint(len(delCodeDict))

    for path in delCodeDict:
        suspicious_var = delCodeDict[path]
        code_decls, ddg_graph = readBuggyCode.parseBuggyFile(path)

        methodName = path.split('<')[1].split('>')[0]
        bugVar = {methodName: delCodeDict[path]}
        bugVarChain = readBuggyCode.varChain(bugVar, ddg_graph, code_decls, path)
        delRefactorCode = bugVarChain.__getattribute__('code')

        # print(path)
        # print(suspicious_var)
        # print(code_decls)
        # print(delRefactorCode)
        # print()
        bugRefactorCodeDict[path] = delRefactorCode

    print(len(bugRefactorCodeDict))
    # bug_edgeList = []
    # for i in bugRefactorCodeDict:
    #     bugRefactorCode = bugRefactorCodeDict[i]
    #     bugDggName = i.split('/')[3].replace('.py','')
    #     bug_edges = render.readCode(bugRefactorCode,bugDggName)
    #     bug_edgeList.append(bug_edges)
    #
    # for i in range(0,len(bug_edgeList)-1):
    #     print(bug_edgeList[i])
    #     result = compareGraph(bug_edgeList[i],bug_edgeList[i+1])

    # addRefactor(bugRefactorCodeDict)

def addRefactor(bugRefactorCodeDict):
    for i in bugRefactorCodeDict:
        path = i.replace('bug.py','fix.py')

        code_decls, ddg_graph = readBuggyCode.parseBuggyFile(path)

        methodName = path.split('<')[1].split('>')[0]
        bugVar = {methodName: addCodeDict[path]}
        addVarChain = readBuggyCode.varChain(bugVar, ddg_graph, code_decls, path)

        addRefactorCode = addVarChain.__getattribute__('code')
        fixRefactorCodeDict[path] = addRefactorCode

    # print(len(fixRefactorCodeDict))

def ddgDiff():
    bug_edgeList = []
    # fix_edgeList = []
    count = 0
    for i in bugRefactorCodeDict:
        j = i.replace('bug.py','fix.py')
        bugRefactorCode = bugRefactorCodeDict[i]
        # fixRefactorCode = fixRefactorCodeDict[j]

        try:
            # if bugRefactorCode != fixRefactorCode:
            bugDggName = i.split('/')[3].replace('.py','')
            # fixDggName = j.split('/')[3].replace('.py','')

            # print(bugRefactorCode)
            # print()
            # print(fixRefactorCode)
            # print()
            # # print('————————————————————————')

            bug_edges = render.readCode(bugRefactorCode,bugDggName)
            count +=1
            print(count,bugDggName)
            print(bugRefactorCode)
            bug_edgeList.append(bug_edges)
            # fix_edges = render.readCode(fixRefactorCode,fixDggName)
            # fix_edgeList.append(fix_edges)
        except:
            pass


    print('bug_edges')
    # same(bug_edges)
    # print('fix_edges')
    # same(fix_edges)

    # print(len(bug_edgeList),len(fix_edgeList))

    for i in range(0,len(bug_edgeList)):
        for j in range(i+1,len(bug_edgeList)):
            result = compareGraph(bug_edgeList[i],bug_edgeList[j])

            if result != '':
                print(i,j)
                print(result)

    # for i in range(0,len(fix_edgeList)):
    #     for j in range(i+1,len(fix_edgeList)):
    #         result = compareGraph(fix_edgeList[i],fix_edgeList[j])
    #
    #         if result != '':
    #             print(i,j)
    #             # print(fix_edgeList[i],fix_edgeList[j])
    #             print(result)


if __name__ == '__main__':
    fileList = getFileList('../testset/quickbugs')
    fileList.sort()

    getLocalVar(fileList)

    # ddgRefactor()
    # ddgDiff()
