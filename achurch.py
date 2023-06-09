from __future__ import annotations
from dataclasses import dataclass
from antlr4 import *
from lcLexer import lcLexer
from lcParser import lcParser
from lcVisitor import lcVisitor

from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
import pydot
import os
import uuid
import shutil
import re


@dataclass
class Variable:
    nom: str


@dataclass
class Abstracio:
    lambdaSymbol: str
    parametre: Variable
    cos: Terme


@dataclass
class Aplicacio:
    funcio: Terme
    argument: Terme


Terme = Variable | Abstracio | Aplicacio


class TreeVisitor(lcVisitor):

    def __init__(self, taula_usuari: dict):
        self.taula_macros = taula_usuari

    def visitParentesis(self, ctx):
        [_, terme, _] = list(ctx.getChildren())
        return self.visit(terme)

    def visitVariable(self, ctx):
        [lletra] = list(ctx.getChildren())
        return Variable(lletra.getText())

    def visitAbstraccio(self, ctx):
        lambdaSymbol, terme = list(ctx.getChildren())[0], list(ctx.getChildren())[-1]
        lletres = list(ctx.LLETRA())
        res = self.visit(terme)
        return currificar(lambdaSymbol, lletres, res)

    def visitAplicacio(self, ctx):
        [terme1, terme2] = list(ctx.getChildren())
        res1 = self.visit(terme1)
        res2 = self.visit(terme2)
        return Aplicacio(res1, res2)
    
    def visitMacro(self, ctx):
        [macro] = list(ctx.getChildren())
        expressio = self.taula_macros[macro.getText()]
        return expressio
    
    def visitInfix(self, ctx):
        [t1, infix, t2] = list(ctx.getChildren())
        res1 = self.visit(t1)
        res2 = self.visit(t2)
        res_infix = self.taula_macros[infix.getText()]
        return Aplicacio(Aplicacio(res_infix,res1), res2)
    
    def visitAssignacio(self, ctx):
        [nomMacro, _, terme] = list(ctx.getChildren())
        self.taula_macros[nomMacro.getText()] = self.visit(terme)
        return None


def currificar(lambdaSymbol, variables, cos):
    if len(variables) == 1:
        return Abstracio(lambdaSymbol.getText(), Variable(variables[0].getText()), cos)
    else:
        return Abstracio(lambdaSymbol.getText(), Variable(variables[0].getText()), currificar(lambdaSymbol, variables[1:], cos))

    
def parenthesize(node):
    match node:
        case Variable(nom):
            return nom
        case Abstracio(lambdaSymbol, parametre, cos):
            return f"({lambdaSymbol}{parenthesize(parametre)}.{parenthesize(cos)})"
        case Aplicacio(funcio, argument):
            return f"({parenthesize(funcio)}{parenthesize(argument)})"
        case _:
            raise ValueError("Node invàlid")



"""
    Substitution rep el node a partir del cual es farà la substitució, el parametre es el valor
    a substituir i el valor es pel node que es substituirà
"""
def substitution(node, parametre, valor):
    match node:
        case Variable(nom):
            if nom == parametre.nom:
                return valor
            else:
                return Variable(nom)
        case Abstracio(lambdaSymbol, param, cos):
            return Abstracio(lambdaSymbol, substitution(param, parametre, valor), substitution(cos, parametre, valor))
        case Aplicacio(funcio, argument):
            return Aplicacio(substitution(funcio, parametre, valor), substitution(argument, parametre, valor))
        case _:
            raise ValueError("Node invàlid")



def betaReduction(node):
    if isinstance(node, Aplicacio) and isinstance(node.funcio, Abstracio):
        return substitution(node.funcio.cos, node.funcio.parametre, node.argument)
    elif isinstance(node, Aplicacio):
        return Aplicacio(betaReduction(node.funcio), betaReduction(node.argument))
    elif isinstance(node, Abstracio):
        return Abstracio(node.lambdaSymbol, node.parametre, betaReduction(node.cos))
    elif isinstance(node, Variable):
        return node
    else:
        raise ValueError("Node invàlid")


"""Retorna el node Aplicacio a partir del cual podem fer una β-reducció en cas que es pugui fer,
   en cas contrari dona None.
"""
def checkBetaReduction(node):
    if isinstance(node, Aplicacio) and isinstance(node.funcio, Abstracio):
        return node
    elif isinstance(node, Aplicacio):
        aux = checkBetaReduction(node.funcio)
        if aux == None: 
            return checkBetaReduction(node.argument)
        else: 
            return aux
    elif isinstance(node, Abstracio): #Afegit rapidament, revisar si es correcte
        return checkBetaReduction(node.cos)
    else:
        return None       


"""
    Retorna una conjunt que conté tots els noms de les variables que hi ha a l'abre o subarbre que té com a arrel
    el node que es passa per paràmetre

"""
def conjuntNoms(node):
    match node:
        case Variable(nom):
            return {nom}
        case Aplicacio(funcio, argument):
            return conjuntNoms(funcio) | conjuntNoms(argument)
        case Abstracio(lambdaSymbol, parametre, cos):
            return conjuntNoms(parametre) | conjuntNoms(cos)
        case _:
            raise ValueError("Node invàlid")



"""
    Retorna una conjunt que conté tots els noms de les variables lligades que hi ha a l'abre o subarbre que té com a arrel
    el node que es passa per paràmetre

"""
def variablesLligades(node):
    match node:
        case Abstracio(_, parametre, cos):
            return {parametre.nom} | variablesLligades(cos)
        case Aplicacio(funcio, argument):
            return variablesLligades(funcio) | variablesLligades(argument)
        case Variable(_):
            return set()
        case _:
            raise ValueError("Node invàlid")


"""
   Aquesta funcio retorna per ordre alfabetic una lletra que no tingui conflicte amb el conjunt
   que es passa per parametre. 
"""
def novaLletra(conflicte):
    lletres_alfabet = "abcdefghijklmnopqrstuvwxyz"

    for lletra in lletres_alfabet:
        if lletra not in conflicte:
            return lletra

    return None


def buscarConflicte(node):
    match node:
        case Aplicacio(funcio, argument):
            dreta = conjuntNoms(argument)
            esquerra = variablesLligades(funcio)
            return esquerra & dreta
        case _:
            return set()


def alphaReduction(node, conflicte):
    lletres_utilitzades = conjuntNoms(node.funcio)
    lletres_utilitzades.add(conflicte)
    nova_lletra = novaLletra(lletres_utilitzades)
    nou_node = Variable(nova_lletra)
    print("α-conversió: " + conflicte + " → " + nova_lletra)
    return Aplicacio(substitution(node.funcio, Variable(conflicte), nou_node), node.argument)


async def redueix(node, limit, update, context):
    final = False
    while not final and limit > 0:
        #Comprobem si podem fer alpha conversió, en cas que si la fem.
        conflicte = buscarConflicte(node)
        if len(conflicte) > 0:
            for i in conflicte:
                node_aux = alphaReduction(node, i)
                print(parenthesize(node.funcio) + " → " + parenthesize(node_aux.funcio))
                missatge = "\n"+ parenthesize(node.funcio) + "→α→" + parenthesize(node_aux.funcio)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=missatge)
                node = node_aux

        #Comprobem si podem fer beta reducció, en cas que si la fem.
        node_aux = checkBetaReduction(node)
        
        if node_aux != None:
            node_reduction = betaReduction(node_aux)
            print("β-reducció:")
            print(parenthesize(node_aux) + " → " + parenthesize(node_reduction))
            missatge = parenthesize(node_aux) + "→β→" + parenthesize(node_reduction)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=missatge)
            node = betaReduction(node)
            await mostrarImatge(node, update, context)
        else:
            final = True
        limit -= 1
        if limit == 0:
            print("...")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="...")
    print("Resultat: ")
    if final:
        print(parenthesize(node))
        missatge = parenthesize(node)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=missatge)
        await mostrarImatge(node, update, context)
    else:
        print("Nothing")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Nothing")
    return missatge


async def mostrarImatge(node: Terme, update: Update, context: ContextTypes.DEFAULT_TYPE):
    graf = pydot.Dot(graph_type="graph", rankdir="TB")

    def crearGraf(node: Terme, pare: Terme = None, id_pare = None, diccionari={}):

        id = str(uuid.uuid4())
        lligada = False
        match node:
            case Variable(nom):
                label = nom
                lligada = diccionari.get(nom)
            case Abstracio(lambdaSymbol, parametre, cos):
                label = lambdaSymbol + parametre.nom
                diccionari[parametre.nom] = id
                crearGraf(cos, node, id, diccionari)
            case Aplicacio(funcio, argument):
                label = "@"
                crearGraf(funcio, node, id, diccionari)
                crearGraf(argument, node, id, diccionari)
        
        pydot_node = pydot.Node(id, label=label, shape="plaintext")
        graf.add_node(pydot_node)

        if pare:
            pydot_edge = pydot.Edge(id_pare, pydot_node)
            graf.add_edge(pydot_edge)
        
        if lligada:
            pydot_edge = pydot.Edge(lligada, pydot_node, style="dotted", dir="back")
            graf.add_edge(pydot_edge)

    crearGraf(node)
    graf.write_png("grafs/"+context.user_data["identificador"]+"/output.png")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("grafs/"+context.user_data["identificador"]+"/output.png", 'rb'))
    netejarDirectori("grafs/"+context.user_data["identificador"]+"/")

def crearIdentificadorAleatori():
    identificador = uuid.uuid4()
    return str(identificador)

"""Crea el directori que s'utilitzarà per tenir magatzem temporal de les imatges que es crearan dels arbres.
   Utilitzen un hash únic com a directori per a que en cas que hi hagin més usuaris tenir aïllat cadascún al
   seu directori.
"""
def prepararDisc(id):
    os.mkdir("grafs/"+str(id))


def netejarDirectori(path):
    arxius = os.listdir(path)
    for arxiu in arxius:
        ruta_arxiu = os.path.join(path, arxiu)
        if os.path.isfile(ruta_arxiu):
            os.remove(ruta_arxiu)

def eliminarDirectori(path):
    if os.path.exists(path): 
        shutil.rmtree(path)


def crearDirectori(path):
    if not os.path.exists(path): 
        os.mkdir(path)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.first_name
    context.user_data["macros"] = dict()
    context.user_data["maxSteps"] = 10
    identificador = crearIdentificadorAleatori()
    context.user_data["identificador"] = identificador
    prepararDisc(identificador)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="AChurchBot!\nBenvolgut "+ username + "!")


async def author(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="@ Marc Gonzalez Vidal, 2023")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="/start\n/help\n/author\n/macros\n/maxSteps numSteps")


async def macros(update: Update, context: ContextTypes.DEFAULT_TYPE):
    missatge = "MACROS"
    for clau, valor in context.user_data["macros"].items():
        missatge += "\n"+ str(clau) + " ≡ " + parenthesize(valor)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=missatge)


async def maxSteps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    error = False
    if text == "/maxSteps":
        await context.bot.send_message(chat_id=update.effective_chat.id, text=str(context.user_data["maxSteps"]))
    elif len(text.split(" ")) == 2: 
        max_steps = text.split(" ")[1]

        regex = r'^[1-9][0-9]*$'
        valid = re.match(regex, max_steps)
        if valid:
            context.user_data["maxSteps"] = int(max_steps)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Límit actualitzat a " + max_steps)
        else:
            error = True
    else:
        error = True
    if error:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Instrucció incorrecta, fes /help per veure com s'ha d'executar")


async def evaluator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lexer = lcLexer(InputStream(update.message.text))
    token_stream = CommonTokenStream(lexer)
    parser = lcParser(token_stream)
    tree = parser.root()
    if parser.getNumberOfSyntaxErrors() == 0:
        visitor = TreeVisitor(context.user_data["macros"])
        arbreSemantic = visitor.visit(tree)
        if arbreSemantic == None:
            missatge = "MACROS"
            for clau, valor in context.user_data["macros"].items():
                print(clau + " ≡ " + parenthesize(valor))
                missatge += "\n"+ str(clau) + " ≡ " + parenthesize(valor)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=missatge)
        else:
            print("Arbre:")
            missatge = parenthesize(arbreSemantic)
            print(missatge)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=missatge)
            await mostrarImatge(arbreSemantic, update, context)
            await redueix(arbreSemantic, context.user_data["maxSteps"], update, context)
    else:
        print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
        print(tree.toStringTree(recog=parser)) 
        await context.bot.send_message(chat_id=update.effective_chat.id, text="La instrucció introduïda és incorrecta")
        missatge = str(parser.getNumberOfSyntaxErrors()) + "errors de sintaxi.\n" + str(tree.toStringTree(recog=parser))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=missatge)

if __name__ == '__main__':
    eliminarDirectori("grafs")
    crearDirectori("grafs")
    TOKEN = "6111049756:AAEDkKcpj-f-wa8tmb9wE8ix-X7xLW11k6s"

    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    author_handler = CommandHandler('author', author)
    help_handler = CommandHandler('help', help)
    macros_handler = CommandHandler('macros', macros)
    maxSteps_handler = CommandHandler('maxSteps', maxSteps)
    evaluator_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), evaluator)
    application.add_handler(start_handler)
    application.add_handler(author_handler)
    application.add_handler(help_handler)
    application.add_handler(macros_handler)
    application.add_handler(maxSteps_handler)
    application.add_handler(evaluator_handler)

    print("Listening...")
    application.run_polling()