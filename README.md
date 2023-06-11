# AChurch - Intèrpret de λ-càlcul (Català)

Benvingut a la pràctica de GEI-LP (edició 2022-2023 Q2) - AChurch! En aquesta pràctica, em implementat un petit intèrpret de λ-càlcul anomenat AChurch utilitzant ANTLR i Python, que funciona a través de Telegram. Aquesta pàgina de README et proporcionarà una visió general del projecte i els passos per utilitzar-lo.

## Què és el λ-càlcul?

El λ-càlcul és un sistema formal desenvolupat per Alonzo Church en la dècada de 1930, que es considera el fonament teòric de la programació funcional. És un model matemàtic que descriu còmput en termes de funcions i substitució de variables.

## Sobre AChurch

AChurch és un intèrpret de λ-càlcul que permetrà als usuaris interactuar amb expressions lambda mitjançant un bot de Telegram. El bot serà capaç d'avaluar les expressions lambda introduïdes pels usuaris i retornar el resultat corresponent, a més d'altres funcionalitats com definir macros i evaluar-les posteriorment.

El funcionament de l'intèrpret AChurch es basa en el parser generat per ANTLR (Another Tool for Language Recognition), que ens ajudarà a analitzar les expressions lambda introduïdes pels usuaris i a construir l'arbre de sintaxi abstracta corresponent.

# Avaluador de Càlcul Lambda
  
Aquest projecte és un bot de Telegram que avalua expressions de càlcul lambda i mostra els passos de reducció i el resultat final. Està construït amb Python i l'analitzador ANTLR4.  
  
## Característiques  
  
- Analitzar i avaluar expressions de càlcul lambda  
- Aplicar reducció alfa i beta  
- Definir i utilitzar macros  
- Limitar el nombre de passos de reducció  
- Mostrar l'arbre d'expressió com una imatge  
  
## Classes  
  
- Variable: Representa una variable en l'expressió de càlcul lambda  
- Abstracio: Representa una abstracció en l'expressió de càlcul lambda  
- Aplicacio: Representa una aplicació en l'expressió de càlcul lambda  
- Terme: Unió de Variable, Abstracio i Aplicacio  
- TreeVisitor: Un visitant per a l'analitzador ANTLR4 per construir l'arbre d'expressió de càlcul lambda  
  
## Funcions  
  
- currificar: Aplica currificació a l'expressió lambda  
- parenthesize: Converteix l'arbre d'expressió a una representació de cadena  
- substitution: Substitueix una variable amb un altre terme en l'expressió  
- betaReduction: Realitza la reducció beta en l'expressió  
- conjuntNoms: Retorna un conjunt de tots els noms de variables en l'arbre d'expressió  
- variablesLligades: Retorna un conjunt de totes les variables lligades en l'arbre d'expressió  
- novaLletra: Retorna un nou nom de variable que evita conflictes amb un conjunt donat  
- cercaAlphaConversion: Cerca i aplica la conversió alfa si cal  
- alphaConversion: Prepara i gestiona el procés de conversió alfa  
- eval: Avalua una expressió i aplica reduccions alfa i beta si cal  
- redueix: Gestiona la reducció de l'expressió  
- mostrarImatge: Genera una imatge de l'arbre d'expressió i l'envia a través de Telegram  
- start, author, help, macros, maxSteps, evaluator: Handlers de comandes del bot de Telegram  
  
## Ús  
1. Compila la gramàtica amb la següent comanda: `antlr4 -Dlanguage=Python3 -no-listener lc.g4`
2. Crea el visitador de la gramàtica amb la següent comanda: `antlr4 -Dlanguage=Python3 -no-listener -visitor lc.g4`
3. Executa el script principal per iniciar el bot: `python achurch.py`  
4. Utilitza el bot de Telegram per enviar expressions de càlcul lambda, definir macros i establir el nombre màxim de passos de reducció.  
5. Per començar a interactuar amb el bot primer feu `/help` per veure les comandes i posteriorment `/start`per inicialitzar el bot.
6. El bot mostrarà els passos de reducció, el resultat final i l'arbre d'expressió com una imatge.

# AChurch - Intérprete de λ-cálculo (Español)  
  
¡Bienvenido a la práctica de GEI-LP (edición 2022-2023 Q2) - AChurch! En esta práctica, hemos implementado un pequeño intérprete de λ-cálculo llamado AChurch utilizando ANTLR y Python, que funciona a través de Telegram. Esta página de README te proporcionará una visión general del proyecto y los pasos para utilizarlo.  
  
## ¿Qué es el λ-cálculo?  
  
El λ-cálculo es un sistema formal desarrollado por Alonzo Church en la década de 1930, que se considera el fundamento teórico de la programación funcional. Es un modelo matemático que describe cómputo en términos de funciones y sustitución de variables.  
  
## Sobre AChurch  
  
AChurch es un intérprete de λ-cálculo que permitirá a los usuarios interactuar con expresiones lambda mediante un bot de Telegram. El bot será capaz de evaluar las expresiones lambda introducidas por los usuarios y retornar el resultado correspondiente, además de otras funcionalidades como definir macros y evaluarlas posteriormente.  
  
El funcionamiento del intérprete AChurch se basa en el parser generado por ANTLR (Another Tool for Language Recognition), que nos ayudará a analizar las expresiones lambda introducidas por los usuarios y a construir el árbol de sintaxis abstracta correspondiente.

# Evaluador de Cálculo Lambda 
  
Este proyecto es un bot de Telegram que evalúa expresiones de cálculo lambda y muestra los pasos de reducción y el resultado final. Está construido con Python y el analizador ANTLR4.  
  
## Características  
  
- Analizar y evaluar expresiones de cálculo lambda  
- Aplicar reducción alfa y beta  
- Definir y utilizar macros  
- Limitar el número de pasos de reducción  
- Mostrar el árbol de expresión como una imagen  
  
## Clases  
  
- Variable: Representa una variable en la expresión de cálculo lambda  
- Abstracio: Representa una abstracción en la expresión de cálculo lambda  
- Aplicacio: Representa una aplicación en la expresión de cálculo lambda  
- Terme: Unión de Variable, Abstracio y Aplicacio  
- TreeVisitor: Un visitante para el analizador ANTLR4 para construir el árbol de expresión de cálculo lambda  
  
## Funciones  
  
- currificar: Aplica currificación a la expresión lambda  
- parenthesize: Convierte el árbol de expresión a una representación de cadena  
- substitution: Sustituye una variable con otro término en la expresión  
- betaReduction: Realiza la reducción beta en la expresión  
- conjuntNoms: Devuelve un conjunto de todos los nombres de variables en el árbol de expresión  
- variablesLligades: Devuelve un conjunto de todas las variables ligadas en el árbol de expresión  
- novaLletra: Devuelve un nuevo nombre de variable que evita conflictos con un conjunto dado  
- cercaAlphaConversion: Busca y aplica la conversión alfa si es necesario  
- alphaConversion: Prepara y gestiona el proceso de conversión alfa  
- eval: Evalúa una expresión y aplica reducciones alfa y beta si es necesario  
- redueix: Gestiona la reducción de la expresión  
- mostrarImatge: Genera una imagen del árbol de expresión y la envía a través de Telegram  
- start, author, help, macros, maxSteps, evaluator: Handlers de comandos del bot de Telegram  
  
## Uso  
  
1. Compila la gramática con el siguiente comando: `antlr4 -Dlanguage=Python3 -no-listener lc.g4`
2. Crea el visitador de la gramática con el siguiente comando: `antlr4 -Dlanguage=Python3 -no-listener -visitor lc.g4`
3. Ejecuta el script principal para iniciar el bot: `python achurch.py`
4. Utiliza el bot de Telegram para enviar expresiones de cálculo lambda, definir macros y establecer el número máximo de pasos de reducción.
5. Para comenzar a interactuar con el bot, primero ejecuta `/help` para ver los comandos y luego `/start` para inicializar el bot.  
6. El bot mostrará los pasos de reducción, el resultado final y el árbol de expresión como una imagen.  
    
  

# AChurch - λ-Calculus Interpreter (English)  
  
Welcome to the GEI-LP practice (2022-2023 Q2 edition) - AChurch! In this practice, we have implemented a small λ-calculus interpreter called AChurch using ANTLR and Python, which operates through Telegram. This README page will provide you with an overview of the project and the steps to use it.  
  
## What is λ-calculus?  
  
The λ-calculus is a formal system developed by Alonzo Church in the 1930s, which is considered the theoretical foundation of functional programming. It is a mathematical model that describes computation in terms of functions and variable substitution.  
  
## About AChurch  
  
AChurch is a λ-calculus interpreter that allows users to interact with lambda expressions via a Telegram bot. The bot will be able to evaluate the lambda expressions entered by users and return the corresponding result, as well as other functionalities such as defining macros and evaluating them later.  
  
The operation of the AChurch interpreter is based on the parser generated by ANTLR (Another Tool for Language Recognition), which will help us analyze the lambda expressions entered by users and construct the corresponding abstract syntax tree.  


# Lambda Calculus Evaluator  
  
This project is a Telegram bot that evaluates lambda calculus expressions and displays the reduction steps and the final result. It is built using Python and the ANTLR4 parser.  
  
## Features  
  
- Parse and evaluate lambda calculus expressions  
- Apply alpha and beta reduction  
- Define and use macros  
- Limit the number of reduction steps  
- Display the expression tree as an image  
  
## Classes  
  
- Variable: Represents a variable in the lambda calculus expression  
- Abstracio: Represents an abstraction in the lambda calculus expression  
- Aplicacio: Represents an application in the lambda calculus expression  
- Terme: A union of Variable, Abstracio, and Aplicacio  
- TreeVisitor: A visitor for the ANTLR4 parser to construct the lambda calculus expression tree  
  
## Functions  
  
- currificar: Curries the lambda expression  
- parenthesize: Converts the expression tree to a string representation  
- substitution: Substitutes a variable with another term in the expression  
- betaReduction: Performs beta reduction on the expression  
- conjuntNoms: Returns a set of all variable names in the expression tree  
- variablesLligades: Returns a set of all bound variables in the expression tree  
- novaLletra: Returns a new variable name that avoids conflicts with a given set  
- cercaAlphaConversion: Searches for and applies alpha conversion if needed  
- alphaConversion: Prepares and manages the alpha conversion process  
- eval: Evaluates an expression and applies alpha and beta reductions if needed  
- redueix: Manages the reduction of the expression  
- mostrarImatge: Generates an image of the expression tree and sends it via Telegram  
- start, author, help, macros, maxSteps, evaluator: Telegram bot command handlers  
  
## Usage  

1. Compile the grammar using the following command: `antlr4 -Dlanguage=Python3 -no-listener lc.g4`
2. Create the grammar visitor using the following command: `antlr4 -Dlanguage=Python3 -no-listener -visitor lc.g4`
3. Run the main script to start the bot: `python achurch.py`
4. Use the Telegram bot to send lambda calculus expressions, define macros, and set the maximum number of reduction steps.
5. To start interacting with the bot, first type `/help` to see the commands and then `/start` to initialize the bot.  
6. The bot will display the reduction steps, the final result, and the expression tree as an image.