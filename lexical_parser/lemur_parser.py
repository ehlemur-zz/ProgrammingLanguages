"""This is the core of the lexical parser.

It implements the parse function, that receives a string with the source code of
the program and generates a list of lexemes.
It also implements a bunch of small parsers, each parser takes care of parsing a
kind of token (e.g. numbers, names, comments) and the parse function just makes
sure everything works.
"""

import string

import lemur_lexeme
import lemur_util

from lemur_state import LemurState



def parse(program):
  """Parses the program as far as possible

  Args:
    program: String. The program to parse.
  Returns:
    A LemurState containing the lexemes, the position, row and column until
    where the program was parsed, and whether the parsing succeded.
  """
  state = LemurState(program=program)

  # Each parser is a combination of two functions. 
  # The cond function tests if the parser is applicable and the second function
  # executes the parser
  # The parser returns an updated state ready to pass to the next one.
  # If the token cannot be parsed (i.e. is a lexical error), the error parser
  # is called.
  # ORDER IS IMPORTANT.

  parsers = [(_string_cond, _string), (_character_cond, _character),
             (_name_cond, _name), (_number_cond, _number),
             (_multiline_comment_cond, _multiline_comment),
             (_comment_cond, _comment), (_newline_cond, _newline),
             (_double_token_cond, _double_token),
             (_single_token_cond, _single_token),
             (_whitespace_cond, _whitespace), (_error_cond, _error)]

  while state.i < len(program):
    for cond, parser in parsers:
      if cond(state):
        state = parser(state)
        break
    if not state.valid:
      break
  return state


# The following two functions parse multiline comments

def _multiline_comment_cond(state):
  return lemur_util.take_two(state) == '/*'
   
def _multiline_comment(state):
  state.i += 2
  state.col += 2
  while state.i < len(state.program):
    if lemur_util.take_two(state) == '*/':
      state.i += 2
      state.col += 2
      return state
    if state.program[state.i] == '\n':
      state.col = 0
      state.row += 1
    state.i += 1
    state.col += 1
  state.valid = False
  return state


# The following two functions parse single line comments

def _comment_cond(state):
  return lemur_util.take_two(state) == '//'

def _comment(state):
  state.i += 2
  state.col += 2
  while state.i < len(state.program):
    if state.program[state.i] == '\n':
      state.i += 1
      state.col = 1
      state.row += 1 
      break
    state.i += 1
    state.col += 1
  return state


# The following two functions parse numbers (real and integers)

def _number_cond(state):
  next_two = lemur_util.take_two(state)
  is_negative = (next_two[0] == '-' and next_two[1] in string.digits)
  return state.program[state.i] in string.digits or is_negative
         

def _number(state):
  start = state.copy()
  seen_dot = False
  if state.program[state.i] == '-':
    state.i += 1
    state.col += 1
  while state.i < len(state.program) and state.program[state.i] != '\n':
    if (state.program[state.i] == '.' and seen_dot) \
       or state.program[state.i] not in string.digits + '.':
      break
    seen_dot = (state.program[state.i] == '.')
    state.i += 1
    state.col += 1
  state.lexemes.append(lemur_lexeme.number(start, state))
  return state


# The following two functions parse strings

def _string_cond(state):
  return state.program[state.i] == '"'

def _string(state):
  state.i += 1
  state.col += 1
  start = state.copy()
  while state.i < len(state.program) and state.program[state.i] != '\n':
    if state.program[state.i-1] != '\\' and state.program[state.i] == '"':
      state.lexemes.append(lemur_lexeme.string(start, state))
      state.i += 2
      state.col += 2
      return state
    state.i += 1
    state.col += 1
  state.valid = False
  return state


# The following two functions parse characters

def _character_cond(state):
  return state.program[state.i] == '\''

def _character(state):
  state.i += 1
  state.col += 1
  start = state.copy()
  if state.program[state.i] == '\\':
    if state.i + 2 >= len(state.program) or state.program[state.i+2] != '\'':
      state.valid = False
      return state
    state.i += 1
    state.col += 1
  elif state.i + 1 >= len(state.program) or state.program[state.i+1] != '\'':
    state.valid = False
    return state
  state.i += 1
  state.lexemes.append(lemur_lexeme.character(start, state))
  state.i += 1
  state.col += 2
  return state


# The following two functions parse names (id's and reserved words)

def _name_cond(state):
  return state.program[state.i] in string.letters

def _name(state):
  start = state.copy()
  while state.i < len(state.program) and state.program[state.i] != '\n':
    if state.program[state.i] not in string.letters + string.digits + '_':
      break
    state.i += 1
    state.col += 1
  state.lexemes.append(lemur_lexeme.name(start, state))
  return state


# The following two functions parse double tokens (==, <=, >=, !=, ||, &&)

def _double_token_cond(state):
  return lemur_util.take_two(state) in lemur_util.DOUBLE_TOKENS

def _double_token(state):
  state.lexemes.append(lemur_lexeme.double_token(state))
  state.i += 2
  state.col += 2
  return state


# The following two functions parse single tokens (+, -, *, /, etc.)

def _single_token_cond(state):
  return state.program[state.i] in lemur_util.SINGLE_TOKENS

def _single_token(state):
  state.lexemes.append(lemur_lexeme.single_token(state))
  state.i += 1
  state.col += 1
  return state


# The following two functions define the error parser.
# The error parser always succeeds. It reports the lexical error on the lexeme
# list and interrupts the parsing.

def _error_cond(state):
  return True

def _error(state):
  state.valid = False
  state.lexemes.append(lemur_lexeme.error(state))
  return state


# The following two functions parse newlines

def _newline_cond(state):
  return state.program[state.i] == '\n'

def _newline(state):
  state.i += 1
  state.col = 1
  state.row += 1
  return state


# The following two functions parse whitespaces

def _whitespace_cond(state):
  return state.program[state.i] in string.whitespace

def _whitespace(state):
  state.i += 1
  state.col += 1
  return state


