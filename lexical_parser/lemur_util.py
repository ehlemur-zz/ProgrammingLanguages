RESERVED_WORDS = (
  'funcion_principal booleano caracter entero real cadena fin_principal leer '
  'imprimir si si_no entonces fin_si mientras hacer fin_mientras para '
  'fin_para seleccionar entre caso romper defecto fin_seleccionar estructura '
  'fin_estructura funcion fin_funcion falso verdadero retornar').split()

DOUBLE_TOKENS = {'==': 'tk_igual', '!=': 'tk_dif', '&&': 'tk_y', '||': 'tk_o',
                 '<=': 'tk_menor_igual', '>=': 'tk_mayor_igual'}

SINGLE_TOKENS = {'+': 'tk_mas', '-': 'tk_menos', '*': 'tk_mult', '/': 'tk_div',
                 '%': 'tk_mod', '=': 'tk_asig', '!': 'tk_neg', ':': 'tk_dosp',
                 '<': 'tk_menor', '>': 'tk_mayor', '\'': 'tk_comilla_sen',
                 '"': 'tk_comilla_dob', ';': 'tk_pyc', ',': 'tk_coma',
                 '(': 'tk_par_izq', ')': 'tk_par_der'}


def take_two(state):
  """Return the next two characters

  Args:
    state: LemurState instance. Contains the program and the position.
  Returns:
    Returns the next two characters or '\x00\x00' if the program is not large
    enough.
  """
  if state.i + 1 > len(state.program):
    return '\x00\x00'
  return state.program[state.i:state.i+2]

