# -*- coding: latin-1 -*-

import lemur_parser

tests = [
"""funcion_principal

    imprimir (3+5);

fin_principal""",

"""funcion_principal
    entero a1 = 5 * 3;
    imprimir( a1 / 10 );
fin_principal
// comentario al final""",

"""/* esto no debe
importar, pero cuenta las lineas
*/
funcion entero sum(entero a, entero b) hacer
    retornar a + b;
    // fin
fin_funcion""",

"""/* esto no debe
importar, pero cuenta las lineas
*/
funcion entero sum(entero a, entero b) hacer
    retornar a + Ñ;
    // fin
fin_funcion"""]


expected_outputs = [
"""<funcion_principal,1,1>
<imprimir,3,5>
<tk_par_izq,3,14>
<tk_entero,3,3,15>
<tk_mas,3,16>
<tk_entero,5,3,17>
<tk_par_der,3,18>
<tk_pyc,3,19>
<fin_principal,5,1>""",

"""<funcion_principal,1,1>
<entero,2,5>
<id,a1,2,12>
<tk_asig,2,15>
<tk_entero,5,2,17>
<tk_mult,2,19>
<tk_entero,3,2,21>
<tk_pyc,2,22>
<imprimir,3,5>
<tk_par_izq,3,13>
<id,a1,3,15>
<tk_div,3,18>
<tk_entero,10,3,20>
<tk_par_der,3,23>
<tk_pyc,3,24>
<fin_principal,4,1>""",

"""<funcion,4,1>
<entero,4,9>
<id,sum,4,16>
<tk_par_izq,4,19>
<entero,4,20>
<id,a,4,27>
<tk_coma,4,28>
<entero,4,30>
<id,b,4,37>
<tk_par_der,4,38>
<hacer,4,40>
<retornar,5,5>
<id,a,5,14>
<tk_mas,5,16>
<id,b,5,18>
<tk_pyc,5,19>
<fin_funcion,7,1>""",

"""<funcion,4,1>
<entero,4,9>
<id,sum,4,16>
<tk_par_izq,4,19>
<entero,4,20>
<id,a,4,27>
<tk_coma,4,28>
<entero,4,30>
<id,b,4,37>
<tk_par_der,4,38>
<hacer,4,40>
<retornar,5,5>
<id,a,5,14>
<tk_mas,5,16>
>>> Error lexico (linea: 5, posicion: 18)"""]


for i, (t, e) in enumerate(zip(tests, expected_outputs)):
  print "Test #%d" % (i + 1)
  r = '\n'.join(lemur_parser.parse(t).lexemes)
  if r != e:
    print " Failed"
    print "  Found"
    print r
    print "  Expected"
    print e
    break
  else:
    print " OK"
  
