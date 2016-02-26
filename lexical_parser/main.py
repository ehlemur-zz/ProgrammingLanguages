import sys
import lemur_parser


# Read from stdin until EOF
program = sys.stdin.read()

# Print the lexemes
print '\n'.join(lemur_parser.parse(program).lexemes)
