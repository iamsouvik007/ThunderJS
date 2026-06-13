from enum import Enum, auto


class TokenType(Enum):
    # Keywords
    LET = auto()
    CONST = auto()

    IF = auto()
    ELSE = auto()

    FOR = auto()
    WHILE = auto()

    FUNCTION = auto()
    RETURN = auto()

    # Literals
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    MOD = auto()
    POWER = auto()

    ASSIGN = auto()

    EQUAL = auto()
    STRICT_EQUAL = auto()

    NOT_EQUAL = auto()
    STRICT_NOT_EQUAL = auto()

    LESS = auto()
    LESS_EQUAL = auto()

    GREATER = auto()
    GREATER_EQUAL = auto()

    AND = auto()
    OR = auto()
    NOT = auto()

    # Delimiters
    LPAREN = auto()
    RPAREN = auto()

    LBRACE = auto()
    RBRACE = auto()

    LBRACKET = auto()
    RBRACKET = auto()

    COMMA = auto()
    DOT = auto()

    SEMICOLON = auto()

    EOF = auto()


class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"