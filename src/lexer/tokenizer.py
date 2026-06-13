from src.lexer.token import Token, TokenType

class Tokenizer:
    KEYWORDS = {
        "let": TokenType.LET,
        "const": TokenType.CONST,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "for": TokenType.FOR,
        "while": TokenType.WHILE,
        "function": TokenType.FUNCTION,
        "return": TokenType.RETURN,
    }

    def __init__(self, source):
        self.source = source
        self.position = 0

    def current_char(self):
        if self.position >= len(self.source):
            return None
        return self.source[self.position]

    def advance(self):
        self.position += 1

    def skip_whitespace(self):
        while (
            self.current_char() is not None
            and self.current_char().isspace()
        ):
            self.advance()

    def read_number(self):
        number = ""

        while (
            self.current_char() is not None
            and self.current_char().isdigit()
        ):
            number += self.current_char()
            self.advance()

        return Token(TokenType.NUMBER, int(number))

    def read_identifier(self):
        identifier = ""

        while (
            self.current_char() is not None
            and (
                self.current_char().isalnum()
                or self.current_char() == "_"
            )
        ):
            identifier += self.current_char()
            self.advance()

        if identifier in self.KEYWORDS:
            return Token(self.KEYWORDS[identifier], identifier)

        return Token(TokenType.IDENTIFIER, identifier)

    def read_string(self):
        quote = self.current_char()
        self.advance()

        value = ""

        while (
            self.current_char() is not None
            and self.current_char() != quote
        ):
            value += self.current_char()
            self.advance()

        self.advance()

        return Token(TokenType.STRING, value)

    def tokenize(self):
        tokens = []

        while self.current_char() is not None:

            self.skip_whitespace()

            current = self.current_char()

            if current is None:
                break

            if current.isdigit():
                tokens.append(self.read_number())
                continue

            if current.isalpha() or current == "_":
                tokens.append(self.read_identifier())
                continue

            if current in ('"', "'"):
                tokens.append(self.read_string())
                continue

            if (
                current == "="
                and self.peek() == "="
                and self.peek(2) == "="
            ):
                tokens.append(
                    Token(TokenType.STRICT_EQUAL, "===")
                )

                self.position += 3
                continue

            

            single_tokens = {
                "+": TokenType.PLUS,
                "-": TokenType.MINUS,
                "*": TokenType.STAR,
                "/": TokenType.SLASH,
                "%": TokenType.MOD,
                "=": TokenType.ASSIGN,
                "<": TokenType.LESS,
                ">": TokenType.GREATER,
                "!": TokenType.NOT,
                "(": TokenType.LPAREN,
                ")": TokenType.RPAREN,
                "{": TokenType.LBRACE,
                "}": TokenType.RBRACE,
                "[": TokenType.LBRACKET,
                "]": TokenType.RBRACKET,
                ",": TokenType.COMMA,
                ".": TokenType.DOT,
                ";": TokenType.SEMICOLON,
            }

            if current in single_tokens:
                tokens.append(
                    Token(
                        single_tokens[current],
                        current
                    )
                )

                self.advance()
                continue


            raise Exception(
                f"Unexpected character: {current}"
            )

        tokens.append(Token(TokenType.EOF))

        return tokens
    
    def peek(self, offset=1):
        pos = self.position + offset

        if pos >= len(self.source):
            return None

        return self.source[pos]
    
    