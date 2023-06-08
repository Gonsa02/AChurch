grammar lc;

root : terme
      | assignacio
      ;

terme : terme terme                       #aplicacio
      | '(' terme ')'                     #parentesis
      | LAMBDA LLETRA+ '.' terme          #abstraccio
      | LLETRA                            #variable
      | MACRO                             #macro
      ;

assignacio : MACRO ASSIGNACIO terme;

MACRO : LLETRAMAJUSCULA (LLETRAMAJUSCULA | DIGIT)*;

LLETRA : [a-z];

LLETRAMAJUSCULA : [A-Z];

DIGIT : [0-9];

LAMBDA : '\\' | 'λ';

ASSIGNACIO : '≡' | '=';


WS : [ \t\r\n]+ -> skip;