from src.lexer.token import TokenType
from src.parser.ast_nodes import (
    Program,
    VariableDeclaration,
    NumberLiteral,
    StringLiteral,
    Identifier,
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        return self.tokens[self.position]

    def advance(self):
        self.position += 1

    def expect(self, token_type):
        token = self.current_token()

        if token.type != token_type:
            raise Exception(
                f"Expected {token_type}, got {token.type}"
            )

        self.advance()

        return token

    def parse(self):
        statements = []

        while self.current_token().type != TokenType.EOF:
            statements.append(
                self.parse_statement()
            )

        return Program(statements)

    def parse_statement(self):
        token = self.current_token()

        if token.type == TokenType.LET:
            return self.parse_variable_declaration()

        raise Exception(
            f"Unexpected token: {token.type}"
        )

    def parse_variable_declaration(self):
        self.expect(TokenType.LET)

        name = self.expect(
            TokenType.IDENTIFIER
        ).value

        self.expect(TokenType.ASSIGN)

        value_token = self.current_token()

        if value_token.type == TokenType.NUMBER:
            value = NumberLiteral(
                value_token.value
            )

        elif value_token.type == TokenType.STRING:
            value = StringLiteral(
                value_token.value
            )

        else:
            raise Exception(
                "Expected number or string"
            )

        self.advance()

        self.expect(TokenType.SEMICOLON)

        return VariableDeclaration(
            name,
            value
        )