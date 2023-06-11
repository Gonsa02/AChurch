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
        return Aplicacio(Aplicacio(res_infix, res1), res2)

    def visitAssignacio(self, ctx):
        [nomMacro, _, terme] = list(ctx.getChildren())
        self.taula_macros[nomMacro.getText()] = self.visit(terme)
        return None


def currificar(lambdaSymbol: str, variables: list, cos: Terme) -> Abstracio:
    if len(variables) == 1:
        return Abstracio(lambdaSymbol.getText(), Variable(variables[0].getText()), cos)
    else:
        return Abstracio(lambdaSymbol.getText(), Variable(variables[0].getText()), currificar(lambdaSymbol, variables[1:], cos))


"""
    Retorna un string que representa l'arbre que té com a arrel
    el node passat per paràmetre
"""


def parenthesize(node: Terme) -> str:
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
    Substitution rep el node a partir del cual es farà la substitució, el conflicte es la Variable
    a substituir i el valor es la Variable  per la que es substituirà
"""


def substitution(node: Terme, conflicte: Variable, valor: Terme) -> Terme:
    match node:
        case Variable(nom):
            if nom == conflicte.nom:
                return valor
            else:
                return Variable(nom)
        case Abstracio(lambdaSymbol, parametre, cos):
            return Abstracio(lambdaSymbol, parametre, substitution(cos, conflicte, valor))
        case Aplicacio(funcio, argument):
            return Aplicacio(substitution(funcio, conflicte, valor), substitution(argument, conflicte, valor))
        case _:
            raise ValueError("Node invàlid")


"""
    Funcio que retorna una versió Beta reduida del node que es pasa per parametre
"""


def betaReduction(node: Terme) -> Terme:
    match node:
        case Aplicacio(funcio, argument):
            if isinstance(funcio, Abstracio):
                return substitution(funcio.cos, funcio.parametre, argument)
            else:
                return Aplicacio(betaReduction(funcio), betaReduction(argument))
        case Abstracio(lambdaSymbol, parametre, cos):
            return Abstracio(lambdaSymbol, parametre, betaReduction(cos))
        case Variable(_):
            return node
        case _:
            raise ValueError("Node invàlid")


"""
    Retorna una conjunt que conté tots els noms de les variables que hi ha a l'abre o subarbre que té com a arrel
    el node que es passa per paràmetre

"""


def conjuntNoms(node: Terme) -> set:
    match node:
        case Variable(nom):
            return {nom}
        case Aplicacio(funcio, argument):
            return conjuntNoms(funcio) | conjuntNoms(argument)
        case Abstracio(_, parametre, cos):
            return conjuntNoms(parametre) | conjuntNoms(cos)
        case _:
            raise ValueError("Node invàlid")


"""
    Retorna una conjunt que conté tots els noms de les variables lligades que hi ha a l'abre o subarbre que té com a arrel
    el node que es passa per paràmetre
"""


def variablesLligades(node: Terme) -> set:
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


def novaLletra(conflicte: set) -> str:
    lletres_alfabet = "abcdefghijklmnopqrstuvwxyz"

    for lletra in lletres_alfabet:
        if lletra not in conflicte:
            return lletra

    return None


"""
    Funció que busca on es pot aplicar la alpha conversió i l'aplica si cal
"""


def cercaAlphaConversion(node: Terme, conflicte: str, valor: str, noms_utilitzats: set[str]) -> tuple[Terme, bool]:
    match node:
        case Variable(_):
            return node, False

        case Aplicacio(funcio, argument):
            nova_funcio, modificat1 = cercaAlphaConversion(funcio, conflicte, valor, noms_utilitzats)
            nou_argument, modificat2 = cercaAlphaConversion(argument, conflicte, valor, noms_utilitzats)
            return Aplicacio(nova_funcio, nou_argument), modificat1 | modificat2

        case Abstracio(lambdaSymbol, parametre, cos):
            if parametre.nom in noms_utilitzats and conflicte in conjuntNoms(cos):
                nou_node = substitution(cos, parametre, Variable(valor))
                print("α-conversió: " + parametre.nom + " → " + valor)
                return Abstracio(lambdaSymbol, Variable(valor), nou_node), True
            else:
                nou_node, modificat = cercaAlphaConversion(cos, conflicte, valor, noms_utilitzats)
                return Abstracio(lambdaSymbol, parametre, nou_node), modificat


"""
    Funció encarregada de preparar i gestionar l'alphaConversió
"""


async def alphaConversion(funcio: Abstracio, argument: Terme, update: Update, context: ContextTypes.DEFAULT_TYPE) -> Terme:
    variables_lligades = variablesLligades(funcio)
    noms_utilitzats = conjuntNoms(argument)

    nova_lletra = novaLletra(variables_lligades | noms_utilitzats)
    alpha_conversio, modificat = cercaAlphaConversion(funcio, funcio.parametre.nom, nova_lletra, noms_utilitzats.difference(funcio.parametre.nom))  # El difference evita alfa conversions innecessàries
    if modificat:
        abans_text = parenthesize(funcio)
        despres_text = parenthesize(alpha_conversio)
        print(abans_text + " → " + despres_text)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=abans_text + "→α→" + despres_text)
    return Aplicacio(alpha_conversio, argument)


"""
    Funció que evalua una expressió i aplica les alfa conversions i beta reduccions
    en cas que de que s'hagi d'aplicar
"""


async def eval(node: Terme, update: Update, context: ContextTypes.DEFAULT_TYPE) -> tuple[Terme, bool]:
    match node:
        case Variable(_):
            return node, False

        case Abstracio(lambdaSymbol, parametre, cos):
            aux, modificat = await eval(cos, update, context)
            return Abstracio(lambdaSymbol, parametre, aux), modificat

        case Aplicacio(funcio, argument):
            if isinstance(funcio, Abstracio):
                alpha_conversio = await alphaConversion(funcio, argument, update, context)
                beta_conversio = betaReduction(alpha_conversio)
                abans_text = parenthesize(Aplicacio(alpha_conversio, argument))
                despres_text = parenthesize(beta_conversio)
                print("β-reducció:\n" + abans_text + " → " + despres_text)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=abans_text + "→β→" + despres_text)
                await mostrarImatge(beta_conversio, update, context)
                return beta_conversio, True
            else:
                aux, modificat = await eval(funcio, update, context)
                if modificat:
                    return Aplicacio(aux, argument), True
                else:
                    aux, modificat = await eval(argument, update, context)
                    return Aplicacio(funcio, aux), modificat


"""
    Funció encarregada de gestionar les reduccions de l'expressió
"""


async def redueix(node: Terme, limit: int, update: Update, context: ContextTypes.DEFAULT_TYPE):
    reduccio, modificat = await eval(node, update, context)

    while modificat and limit > 0:
        limit -= 1
        reduccio, modificat = await eval(reduccio, update, context)

    if limit == 0:
        print("...\nResultat:\nNothing")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="...\nResultat:\nNothing")
    else:
        text = "Resultat:\n" + parenthesize(reduccio)
        print(text)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        await mostrarImatge(reduccio, update, context)


"""
    Funció per crear la imatge de l'arbre a partir de l'arrel donada
"""


async def mostrarImatge(node: Terme, update: Update, context: ContextTypes.DEFAULT_TYPE):
    graf = pydot.Dot(graph_type="graph", rankdir="TB")

    def crearGraf(node: Terme, pare: Terme=None, id_pare=None, diccionari=dict(), nivell=0):
        id = str(uuid.uuid4())
        info_lligada = False
        match node:
            case Variable(nom):
                label = nom
                info_lligada = diccionari.get(nom)

            case Abstracio(lambdaSymbol, parametre, cos):
                label = lambdaSymbol + parametre.nom
                diccionari[parametre.nom] = list((id, nivell))
                crearGraf(cos, node, id, diccionari, nivell+1)

            case Aplicacio(funcio, argument):
                label = "@"
                crearGraf(funcio, node, id, diccionari, nivell+1)
                crearGraf(argument, node, id, diccionari, nivell+1)

        pydot_node = pydot.Node(id, label=label, shape="plaintext")
        graf.add_node(pydot_node)

        if pare:
            pydot_edge = pydot.Edge(id_pare, pydot_node)
            graf.add_edge(pydot_edge)

        if info_lligada and nivell >= info_lligada[1]:
            pydot_edge = pydot.Edge(info_lligada[0], pydot_node, style="dotted", dir="back")
            graf.add_edge(pydot_edge)

    crearGraf(node)
    graf.write_png("grafs/"+context.user_data["identificador"]+"/output.png")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("grafs/" + context.user_data["identificador"] + "/output.png", 'rb'))
    netejarDirectori("grafs/" + context.user_data["identificador"] + "/")


def crearIdentificadorAleatori():
    identificador = uuid.uuid4()
    return str(identificador)


"""
   Crea el directori que s'utilitzarà per tenir magatzem temporal de les imatges que es crearan dels arbres.
   Utilitzen un hash únic com a directori per a que en cas que hi hagin més usuaris tenir aïllat cadascún al
   seu directori.
"""


def prepararDisc(id):
    os.mkdir("grafs/"+str(id))


"""
    Elimina tots els arxius que hi ha dins del directori que està
    a la ruta que es passa per parametre.
"""


def netejarDirectori(path):
    arxius = os.listdir(path)
    for arxiu in arxius:
        ruta_arxiu = os.path.join(path, arxiu)
        if os.path.isfile(ruta_arxiu):
            os.remove(ruta_arxiu)


"""
    Elimina el directori que està a la ruta que es passa per parametre
    en cas que existeixi
"""


def eliminarDirectori(path):
    if os.path.exists(path):
        shutil.rmtree(path)


"""
    Crea un directori a la ruta que es passa per parametre
    en cas que no existeixi
"""


def crearDirectori(path):
    if not os.path.exists(path):
        os.mkdir(path)


"""
    Funció que inicia tot el necessari de la sessió per poder
    guardar l'informació necessaria per dur a terme les funcionalitats
    de l'apliació
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.first_name
    context.user_data["macros"] = dict()
    context.user_data["maxSteps"] = 10
    identificador = crearIdentificadorAleatori()
    context.user_data["identificador"] = identificador
    prepararDisc(identificador)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="AChurchBot!\nBenvolgut " + username + "!")


"""
    Funció que implementa la funcionalitat de mostrar a través
    de telegram l'informació de l'autor
"""


async def author(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="@ Marc Gonzalez Vidal, 2023")


"""
    Funció que implementa la funcionalitat de mostrar a través
    de telegram l'informació de les comandes que hi ha a l'apliació
"""


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    missatge = (
        "/start: Inicia la sessió per a començar a utilitzar el Lambda Càlcul.\n"
        "/help: Mostra totes les comandes del programa.\n"
        "/author: Mostra l'autor del programa.\n"
        "/macros: Mostra una taula amb totes les macros definides de la sessió.\n"
        "/maxSteps (Sense Parametre): Mostra el maxim nombre de reduccions que es faran en l'evaluació de l'expressió. 10 per defecte.\n"
        "/maxSteps numSteps: Limita el màxim nombre de reduccions que es faran en l'evaluació de l'expressió a numSteps.\n"
    )

    await context.bot.send_message(chat_id=update.effective_chat.id, text=missatge)


"""
    Funció que implementa la funcionalitat de mostrar a través
    de telegram les macros definides
"""


async def macros(update: Update, context: ContextTypes.DEFAULT_TYPE):
    missatge = "MACROS"
    for clau, valor in context.user_data["macros"].items():
        missatge += "\n" + str(clau) + " ≡ " + parenthesize(valor)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=missatge)


"""
    Funció que implementa la funcionalitat de mostrar a través
    de telegram el màxim número de reduccions o modificar-lo
    en cas que es vulgui
"""


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


"""
    Funció encarregada de gestionar els inputs de les evaluacions de lambda Càlcul
    que l'usuari introdueixi per terminal.
"""


async def evaluator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lexer = lcLexer(InputStream(update.message.text))
    token_stream = CommonTokenStream(lexer)
    parser = lcParser(token_stream)
    tree = parser.root()
    if parser.getNumberOfSyntaxErrors() == 0:
        visitor = TreeVisitor(context.user_data["macros"])
        arbreSemantic = visitor.visit(tree)
        if arbreSemantic is None:
            missatge = "MACROS"
            for clau, valor in context.user_data["macros"].items():
                print(clau + " ≡ " + parenthesize(valor))
                missatge += "\n" + str(clau) + " ≡ " + parenthesize(valor)
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
    # Es crea aquest directori per a que en cas que hi hagi més d'un usuari, no es sobrescriguin les seues imatges amb un subdirectori de id únic
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
