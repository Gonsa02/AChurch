from __future__ import annotations
from dataclasses import dataclass
from antlr4 import *
from lcLexer import lcLexer
from lcParser import lcParser
from lcVisitor import lcVisitor


@dataclass
class Root:
    cos: Terme


@dataclass
class Variable:
    nom: str


@dataclass
class Parentesis:
    cos: Terme


@dataclass
class Abstracio:
    lambdaSymbol: str
    parametre: str
    cos: Terme


@dataclass
class Aplicacio:
    funcio: Terme
    argument: Terme


Terme = Variable | Parentesis | Abstracio | Aplicacio


def parenthesize(node):
    if isinstance(node, Root):
        return f"({parenthesize(node.cos)})"
    elif isinstance(node, Variable):
        return node.nom
    elif isinstance(node, Parentesis):
        return f"({parenthesize(node.cos)})"
    elif isinstance(node, Abstracio):
        return f"{node.lambdaSymbol}{node.parametre}.({parenthesize(node.cos)})"
    elif isinstance(node, Aplicacio):
        return f"{parenthesize(node.funcio)}{parenthesize(node.argument)}"
    else:
        raise ValueError("Node invalid")

def substitution(node, parametre, valor):
    if isinstance(node, Variable):
        if node.nom == parametre:
            return Variable(valor)  
        else:
            return node
    elif isinstance(node, Parentesis):
        res = substitution(node.cos)
        return Parentesis(res)
    elif isinstance(node, Abstracio):
        res = substitution(node.cos)
        return Terme(res)
    # falta aplicar a la aplicació


def betaReduction(node):
    if isinstance(node, Aplicacio) and isinstance(node.funcio, Abstracio):
        parametre = node.funcio.parametre
        valor = node.argument
        return Root(substitution(node.funcio, parametre, valor))
    else:
        raise ValueError("Node invalid, ha de ser una aplicació i una abstraccio per fer una β-reducció i es " + str(type(node)) + " " + str(type(node.funcio)))

class TreeVisitor(lcVisitor):

    def visitRoot(self, ctx):
        [terme] = list(ctx.getChildren())
        res = self.visit(terme)
        return Root(res)

    def visitParentesis(self, ctx):
        [_, terme, _] = list(ctx.getChildren())
        res = self.visit(terme)
        return Parentesis(res)

    def visitVariable(self, ctx):
        [lletra] = list(ctx.getChildren())
        return Variable(lletra.getText())

    def visitAbstraccio(self, ctx):
        [lambdaSymbol, lletra, _, terme] = list(ctx.getChildren())
        res = self.visit(terme)
        return Abstracio(lambdaSymbol.getText(), lletra.getText(), res)

    def visitAplicacio(self, ctx):
        [terme1, terme2] = list(ctx.getChildren())
        res1 = self.visit(terme1)
        res2 = self.visit(terme2)
        return Aplicacio(res1, res2)


input_stream = InputStream(input('? '))
lexer = lcLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = lcParser(token_stream)
tree = parser.root()
if parser.getNumberOfSyntaxErrors() == 0:
    visitor = TreeVisitor()
    # print(tree.toStringTree(recog=parser))
    arbreSemantic = visitor.visit(tree)
    print("Arbre:")
    print(parenthesize(arbreSemantic))
    print("β-reducció:")
    reduction = betaReduction(arbreSemantic.cos)
    print(reduction)
else: 
    print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
    print(tree.toStringTree(recog=parser))

"""
input_stream = InputStream(input('? '))
while input_stream:
    lexer = lambdaCalculLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = lambdaCalculParser(token_stream)
    tree = parser.root()
    if parser.getNumberOfSyntaxErrors() == 0:
        print("OKEY")
    else: 
        print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
        print(tree.toStringTree(recog=parser))
"""