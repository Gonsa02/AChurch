grammar lc;

root : terme
      | assignacio
      ;

terme : terme terme                       #aplicacio
      | '(' terme ')'                     #parentesis
      | LAMBDA LLETRA+ '.' terme          #abstraccio
      | terme INFIX terme                 #infix
      | LLETRA                            #variable
      | MACRO                             #macro
      ;

assignacio : macros ASSIGNACIO terme;

macros : MACRO | INFIX;

MACRO : LLETRAMAJUSCULA (LLETRAMAJUSCULA | DIGIT)*;

INFIX : '+' | '-' | '*' | '/' | '%' | '&' | '|' | '<' | '>' | ':' | '.' | '@' | '#' | '$' | '^' | '~' | '?' ;

LLETRA : [a-z];

LLETRAMAJUSCULA : [A-Z];

DIGIT : [0-9];

LAMBDA : '\\' | 'λ';

ASSIGNACIO : '≡' | '=';


WS : [ \t\r\n]+ -> skip;