
class LemurState:
  """Contains the relevant information for lexical parsing.

  Attributes:
    row:     int. The current row.
    col:     int. The current col.
    i:       int. The current position.
    valid:   boolean. True iff the input program is a valid program.
    lexemes: list. The list with the lexemes found in parsing.
    program: string. The string containing the source code.
  """

  def __init__(self, row=1, col=1, i=0, valid=True, program=""):
    """Initializes LemurState with the relevant attributes."""
    self.i = i
    self.row = row
    self.col = col
    self.valid = valid
    self.lexemes = []
    self.program = program

  def copy(self):
    """Return a copy of the current state.

    Returns:
      A copy of the current row, col and i."""
    return LemurState(self.row, self.col, self.i)
