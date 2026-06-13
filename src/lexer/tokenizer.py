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
        "true": TokenType.TRUE,
        "false": TokenType.FALSE,
        "null": TokenType.NULL,
        "undefined": TokenType.UNDEFINED,
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

    def peek(self, offset=1):
        pos = self.position + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]

    def skip_whitespace_and_comments(self):
        while self.position < len(self.source):
            c = self.current_char()
            if c is not None and c.isspace():
                self.advance()
            elif c == '/' and self.peek() == '/':
                while self.current_char() is not None and self.current_char() != '\n':
                    self.advance()
            elif c == '/' and self.peek() == '*':
                self.advance()
                self.advance()
                while self.position < len(self.source):
                    if self.current_char() == '*' and self.peek() == '/':
                        self.advance()
                        self.advance()
                        break
                    self.advance()
            else:
                break

    def read_number(self):
        number = ""
        while (
            self.current_char() is not None
            and (self.current_char().isdigit() or self.current_char() == '.')
        ):
            number += self.current_char()
            self.advance()

        if '.' in number:
            return Token(TokenType.NUMBER, float(number))
        return Token(TokenType.NUMBER, int(number))

    def read_identifier(self):
        identifier = ""
        while (
            self.current_char() is not None
            and (self.current_char().isalnum() or self.current_char() == "_")
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
        while self.current_char() is not None and self.current_char() != quote:
            if self.current_char() == '\\':
                self.advance()
                esc = self.current_char()
                if esc == 'n':
                    value += '\n'
                elif esc == 't':
                    value += '\t'
                elif esc == '\\':
                    value += '\\'
                elif esc == quote:
                    value += quote
                else:
                    value += esc
                self.advance()
            else:
                value += self.current_char()
                self.advance()
        self.advance()
        return Token(TokenType.STRING, value)

    def tokenize(self):
        tokens = []

        while self.current_char() is not None:
            self.skip_whitespace_and_comments()
            current = self.current_char()

            if current is None:
                break

            if current.isdigit():
                tokens.append(self.read_number())
                continue

            if current.isalpha() or current == "_":
                tokens.append(self.read_identifier())
                continue

            if current in ('"', "'", '`'):
                tokens.append(self.read_string())
                continue

            # Three-character tokens
            if current == '=' and self.peek() == '=' and self.peek(2) == '=':
                tokens.append(Token(TokenType.STRICT_EQUAL, "==="))
                self.position += 3
                continue

            if current == '!' and self.peek() == '=' and self.peek(2) == '=':
                tokens.append(Token(TokenType.STRICT_NOT_EQUAL, "!=="))
                self.position += 3
                continue

            if current == '.' and self.peek() == '.' and self.peek(2) == '.':
                tokens.append(Token(TokenType.SPREAD, "..."))
                self.position += 3
                continue

            # Two-character tokens
            if current == '*' and self.peek() == '*':
                tokens.append(Token(TokenType.POWER, "**"))
                self.position += 2
                continue

            if current == '+' and self.peek() == '+':
                tokens.append(Token(TokenType.PLUS_PLUS, "++"))
                self.position += 2
                continue

            if current == '+' and self.peek() == '=':
                tokens.append(Token(TokenType.PLUS_ASSIGN, "+="))
                self.position += 2
                continue

            if current == '-' and self.peek() == '=':
                tokens.append(Token(TokenType.MINUS_ASSIGN, "-="))
                self.position += 2
                continue

            if current == '=' and self.peek() == '=':
                tokens.append(Token(TokenType.EQUAL, "=="))
                self.position += 2
                continue

            if current == '!' and self.peek() == '=':
                tokens.append(Token(TokenType.NOT_EQUAL, "!="))
                self.position += 2
                continue

            if current == '<' and self.peek() == '=':
                tokens.append(Token(TokenType.LESS_EQUAL, "<="))
                self.position += 2
                continue

            if current == '>' and self.peek() == '=':
                tokens.append(Token(TokenType.GREATER_EQUAL, ">="))
                self.position += 2
                continue

            if current == '&' and self.peek() == '&':
                tokens.append(Token(TokenType.AND, "&&"))
                self.position += 2
                continue

            if current == '|' and self.peek() == '|':
                tokens.append(Token(TokenType.OR, "||"))
                self.position += 2
                continue

            # Single-character tokens
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
                tokens.append(Token(single_tokens[current], current))
                self.advance()
                continue

            raise Exception(f"Unexpected character: {current}")

        tokens.append(Token(TokenType.EOF))
        return tokens