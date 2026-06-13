from src.lexer.token import TokenType
from src.parser.ast_nodes import (
    Program,
    VariableDeclaration,
    NumberLiteral,
    StringLiteral,
    Identifier,
    BinaryExpression,
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

        value = self.parse_expression()

        self.expect(TokenType.SEMICOLON)

        return VariableDeclaration(
            name,
            value
        )

    def parse_expression(self):
        left_token = self.current_token()

        if left_token.type == TokenType.NUMBER:
            left = NumberLiteral(left_token.value)

        elif left_token.type == TokenType.STRING:
            left = StringLiteral(left_token.value)

        elif left_token.type == TokenType.IDENTIFIER:
            left = Identifier(left_token.value)

        else:
            raise Exception(
                f"Invalid expression: {left_token.type}"
            )

        # Move past left operand
        self.advance()

        # Simple expression (e.g. let x = 10;)
        if self.current_token().type == TokenType.SEMICOLON:
            return left

        current = self.current_token()

        if current.type in (
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.STAR,
            TokenType.SLASH,
            TokenType.MOD,
            TokenType.STRICT_EQUAL,
        ):
            operator = current.value

            self.advance()

            right_token = self.current_token()

            if right_token.type == TokenType.NUMBER:
                right = NumberLiteral(
                    right_token.value
                )

            elif right_token.type == TokenType.STRING:
                right = StringLiteral(
                    right_token.value
                )

            elif right_token.type == TokenType.IDENTIFIER:
                right = Identifier(
                    right_token.value
                )

            else:
                raise Exception(
                    f"Invalid right operand: {right_token.type}"
                )

            self.advance()

            return BinaryExpression(
                left,
                operator,
                right
            )

        return left