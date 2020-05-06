from enum import Enum, auto

# Tracking for printing convienicence in the scanner / lexxer
global max_width_of_enum
max_width_of_enum = 0

class Token():
    def __init__(self, token_type, lexeme, literal, line):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        global max_width_of_enum
        max_width_of_enum = max(max_width_of_enum, len(self.token_type.name))


    def __str__(self):
        # desired_width = 22
        return 'line: {3}, {0} {4} : {1} : {2}'.format(
            self.token_type, self.lexeme, self.literal, self.line, 
            " " * (max_width_of_enum - len(self.token_type.name)))
        # return '{0} : {1} : {2}'.format(self.token_type, self.lexeme, self.literal)


class TokenType(Enum):
    # Single-character tokens
    OPEN_PAREN, CLOSE_PAREN, OPEN_BRACE, CLOSE_BRACE = auto(), auto(), auto(), auto()
    COMMA, DOT, MINUS, PLUS = auto(), auto(), auto(), auto()
    SEMICOLON, SLASH, STAR = auto(), auto(), auto()

    # One or two character tokens                  
    BANG, BANG_EQUAL = auto(), auto()
    EQUAL, EQUAL_EQUAL = auto(), auto()                
    GREATER, GREATER_EQUAL = auto(), auto()
    LESS, LESS_EQUAL = auto(), auto()

    # Literals                                     
    IDENTIFIER, STRING, NUMBER = auto(), auto(), auto()

    # Keywords                                     
    AND, CLASS, ELSE, FALSE, FUN = auto(), auto(), auto(), auto(), auto()
    FOR, IF, NIL, OR, PRINT = auto(), auto(), auto(), auto(), auto()
    RETURN, SUPER, THIS, TRUE, VAR, WHILE = auto(), auto(), auto(), auto(), auto(), auto()

    # Special
    EOF = auto()