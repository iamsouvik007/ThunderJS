from src.lexer.token import TokenType
from src.parser.ast_nodes import (
    Program,
    VariableDeclaration,
    NumberLiteral,
    StringLiteral,
    BooleanLiteral,
    NullLiteral,
    Identifier,
    BinaryExpression,
    AssignmentExpression,
    UpdateExpression,
    IfStatement,
    CallExpression,
    MemberExpression,
    ForStatement,
    WhileStatement,
    FunctionDeclaration,
    ReturnStatement,
    ArrayLiteral,
    SpreadElement,
    ExpressionStatement,
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
            raise Exception(f"Expected {token_type}, got {token.type}")
        self.advance()
        return token

    def parse(self):
        statements = []
        while self.current_token().type != TokenType.EOF:
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        token = self.current_token()

        if token.type in (TokenType.LET, TokenType.CONST):
            return self.parse_variable_declaration()

        if token.type == TokenType.IF:
            return self.parse_if_statement()

        if token.type == TokenType.FOR:
            return self.parse_for_statement()

        if token.type == TokenType.WHILE:
            return self.parse_while_statement()

        if token.type == TokenType.FUNCTION:
            return self.parse_function_declaration()

        if token.type == TokenType.RETURN:
            return self.parse_return_statement()

        return self.parse_expression_statement()

    def parse_variable_declaration(self):
        self.advance()  # skip let/const
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        if self.current_token().type == TokenType.SEMICOLON:
            self.advance()
        return VariableDeclaration(name, value)

    def parse_expression_statement(self):
        expr = self.parse_expression()
        if self.current_token().type == TokenType.SEMICOLON:
            self.advance()
        return ExpressionStatement(expr)

    def parse_expression(self):
        return self.parse_assignment()

    def parse_assignment(self):
        expr = self.parse_or()

        if isinstance(expr, Identifier):
            if self.current_token().type == TokenType.ASSIGN:
                self.advance()
                value = self.parse_expression()
                return AssignmentExpression(expr.name, "=", value)
            if self.current_token().type == TokenType.PLUS_ASSIGN:
                self.advance()
                value = self.parse_expression()
                return AssignmentExpression(expr.name, "+=", value)
            if self.current_token().type == TokenType.MINUS_ASSIGN:
                self.advance()
                value = self.parse_expression()
                return AssignmentExpression(expr.name, "-=", value)

        return expr

    def parse_or(self):
        left = self.parse_and()
        while self.current_token().type == TokenType.OR:
            self.advance()
            right = self.parse_and()
            left = BinaryExpression(left, "||", right)
        return left

    def parse_and(self):
        left = self.parse_equality()
        while self.current_token().type == TokenType.AND:
            self.advance()
            right = self.parse_equality()
            left = BinaryExpression(left, "&&", right)
        return left

    def parse_equality(self):
        left = self.parse_comparison()
        while self.current_token().type in (
            TokenType.STRICT_EQUAL, TokenType.STRICT_NOT_EQUAL,
            TokenType.EQUAL, TokenType.NOT_EQUAL,
        ):
            operator = self.current_token().value
            self.advance()
            right = self.parse_comparison()
            left = BinaryExpression(left, operator, right)
        return left

    def parse_comparison(self):
        left = self.parse_additive()
        while self.current_token().type in (
            TokenType.LESS, TokenType.LESS_EQUAL,
            TokenType.GREATER, TokenType.GREATER_EQUAL,
        ):
            operator = self.current_token().value
            self.advance()
            right = self.parse_additive()
            left = BinaryExpression(left, operator, right)
        return left

    def parse_additive(self):
        left = self.parse_multiplicative()
        while self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token().value
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryExpression(left, operator, right)
        return left

    def parse_multiplicative(self):
        left = self.parse_exponent()
        while self.current_token().type in (TokenType.STAR, TokenType.SLASH, TokenType.MOD):
            operator = self.current_token().value
            self.advance()
            right = self.parse_exponent()
            left = BinaryExpression(left, operator, right)
        return left

    def parse_exponent(self):
        base = self.parse_unary()
        if self.current_token().type == TokenType.POWER:
            self.advance()
            exp = self.parse_exponent()  # right-associative
            return BinaryExpression(base, "**", exp)
        return base

    def parse_unary(self):
        if self.current_token().type == TokenType.NOT:
            self.advance()
            operand = self.parse_unary()
            return BinaryExpression(operand, "!", None)
        if self.current_token().type == TokenType.MINUS:
            self.advance()
            operand = self.parse_unary()
            return BinaryExpression(NumberLiteral(0), "-", operand)
        return self.parse_postfix()

    def parse_postfix(self):
        expr = self.parse_call_member()

        if isinstance(expr, Identifier) and self.current_token().type == TokenType.PLUS_PLUS:
            self.advance()
            return UpdateExpression(expr.name, "++")

        return expr

    def parse_call_member(self):
        expr = self.parse_primary()

        while True:
            if self.current_token().type == TokenType.DOT:
                self.advance()
                prop = self.expect(TokenType.IDENTIFIER).value
                expr = MemberExpression(expr, prop)
            elif self.current_token().type == TokenType.LBRACKET:
                self.advance()
                prop = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                expr = MemberExpression(expr, prop, computed=True)
            elif self.current_token().type == TokenType.LPAREN:
                expr = self.parse_call(expr)
            else:
                break

        return expr

    def parse_call(self, callee):
        self.expect(TokenType.LPAREN)
        args = []
        if self.current_token().type != TokenType.RPAREN:
            args.append(self.parse_expression())
            while self.current_token().type == TokenType.COMMA:
                self.advance()
                args.append(self.parse_expression())
        self.expect(TokenType.RPAREN)
        return CallExpression(callee, args)

    def parse_primary(self):
        token = self.current_token()

        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberLiteral(token.value)

        if token.type == TokenType.STRING:
            self.advance()
            return StringLiteral(token.value)

        if token.type == TokenType.TRUE:
            self.advance()
            return BooleanLiteral(True)

        if token.type == TokenType.FALSE:
            self.advance()
            return BooleanLiteral(False)

        if token.type == TokenType.NULL:
            self.advance()
            return NullLiteral()

        if token.type == TokenType.UNDEFINED:
            self.advance()
            return NullLiteral()

        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return Identifier(token.value)

        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr

        if token.type == TokenType.LBRACKET:
            return self.parse_array_literal()

        if token.type == TokenType.SPREAD:
            self.advance()
            argument = self.parse_expression()
            return SpreadElement(argument)

        raise Exception(f"Unexpected token: {token.type} ({token.value})")

    def parse_array_literal(self):
        self.expect(TokenType.LBRACKET)
        elements = []
        while self.current_token().type != TokenType.RBRACKET:
            if self.current_token().type == TokenType.SPREAD:
                self.advance()
                elements.append(SpreadElement(self.parse_expression()))
            else:
                elements.append(self.parse_expression())
            if self.current_token().type == TokenType.COMMA:
                self.advance()
        self.expect(TokenType.RBRACKET)
        return ArrayLiteral(elements)

    def parse_block(self):
        self.expect(TokenType.LBRACE)
        statements = []
        while self.current_token().type != TokenType.RBRACE:
            statements.append(self.parse_statement())
        self.expect(TokenType.RBRACE)
        return statements

    def parse_if_statement(self):
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        then_branch = self.parse_block()

        else_branch = None
        if self.current_token().type == TokenType.ELSE:
            self.advance()
            if self.current_token().type == TokenType.IF:
                else_branch = [self.parse_if_statement()]
            else:
                else_branch = self.parse_block()

        return IfStatement(condition, then_branch, else_branch)

    def parse_for_statement(self):
        self.expect(TokenType.FOR)
        self.expect(TokenType.LPAREN)

        # init
        if self.current_token().type in (TokenType.LET, TokenType.CONST):
            init = self.parse_variable_declaration()
        else:
            init = self.parse_expression_statement()

        # test
        test = self.parse_expression()
        self.expect(TokenType.SEMICOLON)

        # update
        update = self.parse_expression()
        self.expect(TokenType.RPAREN)

        body = self.parse_block()
        return ForStatement(init, test, update, body)

    def parse_while_statement(self):
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        test = self.parse_expression()
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return WhileStatement(test, body)

    def parse_function_declaration(self):
        self.expect(TokenType.FUNCTION)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.LPAREN)
        params = []
        if self.current_token().type != TokenType.RPAREN:
            params.append(self.expect(TokenType.IDENTIFIER).value)
            while self.current_token().type == TokenType.COMMA:
                self.advance()
                params.append(self.expect(TokenType.IDENTIFIER).value)
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return FunctionDeclaration(name, params, body)

    def parse_return_statement(self):
        self.expect(TokenType.RETURN)
        value = None
        if self.current_token().type not in (TokenType.SEMICOLON, TokenType.RBRACE):
            value = self.parse_expression()
        if self.current_token().type == TokenType.SEMICOLON:
            self.advance()
        return ReturnStatement(value)
