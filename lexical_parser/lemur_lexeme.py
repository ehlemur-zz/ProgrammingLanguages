"""Some functions to transform the LemurState into string lexemes.

These functions take one or two LemurStates and generate the string
representation of the lexemes. The first state usually contains the starting 
position and the second state the ending one.
"""

import lemur_util


_ERROR_TEMPLATE = '>>> Error lexico (linea: %d, posicion: %d)'
_LEXEME_TEMPLATE = '<%s,%d,%d>'
_NAMED_LEXEME_TEMPLATE = '<%s,%s,%d,%d>'


def _data(start, state):
  """Extract the token from the program.

  Args:
    start: LemurState. Contains the starting position.
    state: LemurState. Contains the ending position.
  Returns:
    The token from the program.
  """
  return state.program[start.i:state.i]

def _lexeme(name, state):
  """The string representation of the lexeme.

  Args:
    name: string. The name of the lexeme (e.g. tk_menos)
    state: LemurState. The row and the column of the lexeme.
  Returns:
    The string representation of the lexeme in the format <lexeme_name,row,col>
    for example <tk_menos,10,33>.
  """
  return _LEXEME_TEMPLATE % (name, state.row, state.col)

def _named_lexeme(name, start, state):
  """The string representation of the lexeme.

  Args:
    name: string. The name of the lexeme (e.g. id, entero)
    start: LemurState. Contains the row, the column and the starting position of
           the lexeme in the program.
    state: LemurState. Contains the ending position of the lexeme.
  Returns:
    The string representation of the lexeme in the format
    <lexeme_name,lexeme,row,col> for example <cadena,"Hola mundo",3,5>.
  """ 
  return _NAMED_LEXEME_TEMPLATE % (name, _data(start, state), start.row,
                                   start.col)

def string(start, state):
  """The string representation of a string lexeme.

  Args:
    start: LemurState. Contains the row, the column and the starting position of
           the lexeme in the program.
    state: LemurState. Contains the ending position of the lexeme.
  Returns:
    The string representation of the lexeme in the format
    <cadena,string,row,col> for example <cadena,"Hola mundo",3,5>.
  """
  return _named_lexeme('tk_cadena', start, state)
  
def character(start, state):
  """The string representation of a character lexeme.

  Args:
    start: LemurState. Contains the row, the column and the starting position of
           the lexeme in the program.
    state: LemurState. Contains the ending position of the lexeme.
  Returns:
    The string representation of the lexeme in the format
    <caracter,character,row,col> for example <caracter,'A',3,5>.
  """
  return _named_lexeme('tk_caracter', start, state)

def number(start, state):
  """The string representation of a number lexeme.

  Args:
    start: LemurState. Contains the row, the column and the starting position of
           the lexeme in the program.
    state: LemurState. Contains the ending position of the lexeme.
  Returns:
    The string representation of the lexeme in the format
    <entero|real,lexeme,row,col> for example <real,-3.1,2,5> or <entero,1,1,1>.
  """
  if '.' in _data(start, state):
    return _named_lexeme('tk_real', start, state)
  return _named_lexeme('tk_entero', start, state)

def name(start, state):
  """The string representation of an id or reserved word lexeme.

  Args:
    start: LemurState. Contains the row, the column and the starting position of
           the lexeme in the program.
    state: LemurState. Contains the ending position of the lexeme.
  Returns:
    The string representation of the lexeme in the format
    <id,name,row,col> for example <id,foo,3,4> or
    <reserved_word,row,col> for example <funcion_principal,1,1>.
  """
  if _data(start, state) in lemur_util.RESERVED_WORDS:
    return _lexeme(_data(start, state), start)
  return _named_lexeme('id', start, state)

def single_token(state):
  """The string representation of a single token lexeme.

  Args:
    state: LemurState. Contains the row, column and position of the lexeme.
  Returns:
    The string representation of the lexeme in the format
    <token,row,col> for example <tk_menos,1,1>.
  """
  token_name = lemur_util.SINGLE_TOKENS[state.program[state.i]]
  return _lexeme(token_name, state)

def double_token(state):
  """The string representation of a double token lexeme.

  Args:
    state: LemurState. Contains the row, column and position of the lexeme.
  Returns:
    The string representation of the lexeme in the format
    <token,row,col> for example <tk_igual,1,1>.
  """
  token_name = lemur_util.SINGLE_TOKENS[lemur_util.take_two(state)]
  return _lexeme(token_name, state)

def error(state):
  """Reports the row and column where an error occurred.

  Args:
    state: LemurState. Contains the row and column of the error.
  Returns:
    The error in the format
    >>> Error lexico (linea: row, posicion: col)
  """
  return _ERROR_TEMPLATE % (state.row, state.col)
