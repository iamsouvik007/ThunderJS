from src.lexer.token import TokenType
from src.parser.ast_nodes import (
    Program,
    VariableDeclaration,
    NumberLiteral,
    StringLiteral,
    BooleanLiteral,
    NullLiteral,
    UndefinedLiteral,
    Identifier,
    BinaryExpression,
    UnaryExpression,
    AssignmentExpression,
    UpdateExpression,
    IfStatement,
    CallExpression,
    MemberExpression,
    ForStatement,
    WhileStatement,
    DoWhileStatement,
    SwitchStatement,
    SwitchCase,
    BreakStatement,
    ContinueStatement,
    FunctionDeclaration,
    FunctionExpression,
    ArrowFunction,
    ReturnStatement,
    ArrayLiteral,
    ObjectLiteral,
    ObjectProperty,
    SpreadElement,
    ExpressionStatement,
    ConditionalExpression,
    TypeofExpression,
    NewExpression,
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        return self.tokens[self.position]

    def peek_token(self, offset=1):
        pos = self.position + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]

    def advance(self):
        self.position += 1

    def expect(self, token_type):
        token = self.current_token()
        if token.type != token_type:
            raise Exception(f"Expected {token_type}, got {token.type}")
        self.advance()
        return token

    def eat_semicolon(self):
        if self.current_token().type == TokenType.SEMICOLON:
            self.advance()

    def parse(self):
        statements = []
        while self.current_token().type != TokenType.EOF:
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        token = self.current_token()

        if token.type in (TokenType.LET, TokenType.CONST, TokenType.VAR):
            return self.parse_variable_declaration()

        if token.type == TokenType.IF:
            return self.parse_if_statement()

        if token.type == TokenType.FOR:
            return self.parse_for_statement()

        if token.type == TokenType.WHILE:
            return self.parse_while_statement()

        if token.type == TokenType.DO:
            return self.parse_do_while_statement()

        if token.type == TokenType.SWITCH:
            return self.parse_switch_statement()

        if token.type == TokenType.FUNCTION:
            return self.parse_function_declaration()

        if token.type == TokenType.RETURN:
            return self.parse_return_statement()

        if token.type == TokenType.BREAK:
            self.advance()
            self.eat_semicolon()
            return BreakStatement()

        if token.type == TokenType.CONTINUE:
            self.advance()
            self.eat_semicolon()
            return ContinueStatement()

        if token.type == TokenType.LBRACE:
            stmts = self.parse_block()
            return ExpressionStatement(NullLiteral())  # bare block, treat as noop

        return self.parse_expression_statement()

    def parse_variable_declaration(self):
        self.advance()  # skip let/const/var
        name = self.expect(TokenType.IDENTIFIER).value

        if self.current_token().type == TokenType.ASSIGN:
            self.advance()
            value = self.parse_expression()
        else:
            value = UndefinedLiteral()

        self.eat_semicolon()
        return VariableDeclaration(name, value)

    def parse_expression_statement(self):
        expr = self.parse_expression()
        self.eat_semicolon()
        return ExpressionStatement(expr)

    def parse_expression(self):
        return self.parse_assignment()

    def parse_assignment(self):
        expr = self.parse_ternary()

        if self.current_token().type in (
            TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN,
            TokenType.STAR_ASSIGN, TokenType.SLASH_ASSIGN, TokenType.MOD_ASSIGN,
        ):
            op = self.current_token().value
            self.advance()
            value = self.parse_assignment()
            return AssignmentExpression(expr, op, value)

        return expr

    def parse_ternary(self):
        expr = self.parse_or()

        if self.current_token().type == TokenType.QUESTION:
            self.advance()
            consequent = self.parse_assignment()
            self.expect(TokenType.COLON)
            alternate = self.parse_assignment()
            return ConditionalExpression(expr, consequent, alternate)

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
            exp = self.parse_exponent()
            return BinaryExpression(base, "**", exp)
        return base

    def parse_unary(self):
        if self.current_token().type == TokenType.NOT:
            self.advance()
            operand = self.parse_unary()
            return UnaryExpression("!", operand)
        if self.current_token().type == TokenType.MINUS:
            self.advance()
            operand = self.parse_unary()
            return UnaryExpression("-", operand)
        if self.current_token().type == TokenType.PLUS:
            self.advance()
            operand = self.parse_unary()
            return UnaryExpression("+", operand)
        if self.current_token().type == TokenType.TYPEOF:
            self.advance()
            operand = self.parse_unary()
            return TypeofExpression(operand)
        if self.current_token().type == TokenType.PLUS_PLUS:
            self.advance()
            expr = self.parse_call_member()
            if isinstance(expr, Identifier):
                return UpdateExpression(expr.name, "++", prefix=True)
            return UpdateExpression(expr, "++", prefix=True)
        if self.current_token().type == TokenType.MINUS_MINUS:
            self.advance()
            expr = self.parse_call_member()
            if isinstance(expr, Identifier):
                return UpdateExpression(expr.name, "--", prefix=True)
            return UpdateExpression(expr, "--", prefix=True)
        if self.current_token().type == TokenType.NEW:
            return self.parse_new_expression()
        return self.parse_postfix()

    def parse_new_expression(self):
        self.expect(TokenType.NEW)
        callee = self.parse_call_member()
        if isinstance(callee, CallExpression):
            return NewExpression(callee.callee, callee.arguments)
        return NewExpression(callee, [])

    def parse_postfix(self):
        expr = self.parse_call_member()

        if isinstance(expr, Identifier) and self.current_token().type == TokenType.PLUS_PLUS:
            self.advance()
            return UpdateExpression(expr.name, "++", prefix=False)

        if isinstance(expr, Identifier) and self.current_token().type == TokenType.MINUS_MINUS:
            self.advance()
            return UpdateExpression(expr.name, "--", prefix=False)

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
            if self.current_token().type == TokenType.SPREAD:
                self.advance()
                args.append(SpreadElement(self.parse_assignment()))
            else:
                args.append(self.parse_assignment())
            while self.current_token().type == TokenType.COMMA:
                self.advance()
                if self.current_token().type == TokenType.SPREAD:
                    self.advance()
                    args.append(SpreadElement(self.parse_assignment()))
                else:
                    args.append(self.parse_assignment())
        self.expect(TokenType.RPAREN)
        return CallExpression(callee, args)

    def is_arrow_function(self):
        if self.current_token().type == TokenType.IDENTIFIER and self.peek_token().type == TokenType.ARROW:
            return True
        if self.current_token().type == TokenType.LPAREN:
            saved = self.position
            depth = 0
            while self.position < len(self.tokens):
                t = self.current_token().type
                if t == TokenType.LPAREN:
                    depth += 1
                elif t == TokenType.RPAREN:
                    depth -= 1
                    if depth == 0:
                        self.position += 1
                        result = self.current_token().type == TokenType.ARROW
                        self.position = saved
                        return result
                elif t in (TokenType.LBRACE, TokenType.SEMICOLON, TokenType.EOF):
                    break
                self.position += 1
            self.position = saved
        return False

    def parse_arrow_function(self):
        params = []
        if self.current_token().type == TokenType.IDENTIFIER:
            params.append(self.current_token().value)
            self.advance()
        else:
            self.expect(TokenType.LPAREN)
            if self.current_token().type != TokenType.RPAREN:
                if self.current_token().type == TokenType.SPREAD:
                    self.advance()
                    params.append("..." + self.expect(TokenType.IDENTIFIER).value)
                else:
                    params.append(self.expect(TokenType.IDENTIFIER).value)
                while self.current_token().type == TokenType.COMMA:
                    self.advance()
                    if self.current_token().type == TokenType.SPREAD:
                        self.advance()
                        params.append("..." + self.expect(TokenType.IDENTIFIER).value)
                    else:
                        params.append(self.expect(TokenType.IDENTIFIER).value)
            self.expect(TokenType.RPAREN)
        self.expect(TokenType.ARROW)

        if self.current_token().type == TokenType.LBRACE:
            body = self.parse_block()
        else:
            body = self.parse_assignment()

        return ArrowFunction(params, body)

    def parse_primary(self):
        token = self.current_token()

        if self.is_arrow_function():
            return self.parse_arrow_function()

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
            return UndefinedLiteral()

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

        if token.type == TokenType.LBRACE:
            return self.parse_object_literal()

        if token.type == TokenType.FUNCTION:
            return self.parse_function_expression()

        if token.type == TokenType.SPREAD:
            self.advance()
            argument = self.parse_assignment()
            return SpreadElement(argument)

        raise Exception(f"Unexpected token: {token.type} ({token.value})")

    def parse_function_expression(self):
        self.expect(TokenType.FUNCTION)
        name = None
        if self.current_token().type == TokenType.IDENTIFIER:
            name = self.current_token().value
            self.advance()
        self.expect(TokenType.LPAREN)
        params = []
        if self.current_token().type != TokenType.RPAREN:
            if self.current_token().type == TokenType.SPREAD:
                self.advance()
                params.append("..." + self.expect(TokenType.IDENTIFIER).value)
            else:
                params.append(self.expect(TokenType.IDENTIFIER).value)
            while self.current_token().type == TokenType.COMMA:
                self.advance()
                if self.current_token().type == TokenType.SPREAD:
                    self.advance()
                    params.append("..." + self.expect(TokenType.IDENTIFIER).value)
                else:
                    params.append(self.expect(TokenType.IDENTIFIER).value)
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return FunctionExpression(name, params, body)

    def parse_array_literal(self):
        self.expect(TokenType.LBRACKET)
        elements = []
        while self.current_token().type != TokenType.RBRACKET:
            if self.current_token().type == TokenType.SPREAD:
                self.advance()
                elements.append(SpreadElement(self.parse_assignment()))
            elif self.current_token().type == TokenType.COMMA:
                elements.append(UndefinedLiteral())
            else:
                elements.append(self.parse_assignment())
            if self.current_token().type == TokenType.COMMA:
                self.advance()
        self.expect(TokenType.RBRACKET)
        return ArrayLiteral(elements)

    def parse_object_literal(self):
        self.expect(TokenType.LBRACE)
        properties = []
        while self.current_token().type != TokenType.RBRACE:
            if self.current_token().type == TokenType.SPREAD:
                self.advance()
                properties.append(SpreadElement(self.parse_assignment()))
            elif self.current_token().type == TokenType.LBRACKET:
                self.advance()
                key = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                self.expect(TokenType.COLON)
                value = self.parse_assignment()
                properties.append(ObjectProperty(key, value, computed=True))
            elif self.current_token().type in (TokenType.IDENTIFIER, TokenType.STRING, TokenType.NUMBER):
                key_token = self.current_token()
                self.advance()
                if key_token.type == TokenType.IDENTIFIER and self.current_token().type == TokenType.LPAREN:
                    params = self._parse_param_list()
                    body = self.parse_block()
                    func = FunctionExpression(key_token.value, params, body)
                    properties.append(ObjectProperty(StringLiteral(key_token.value), func))
                elif self.current_token().type == TokenType.COLON:
                    self.advance()
                    value = self.parse_assignment()
                    if key_token.type == TokenType.NUMBER:
                        properties.append(ObjectProperty(NumberLiteral(key_token.value), value))
                    else:
                        key_str = key_token.value if isinstance(key_token.value, str) else str(key_token.value)
                        properties.append(ObjectProperty(StringLiteral(key_str), value))
                else:
                    properties.append(ObjectProperty(StringLiteral(key_token.value), Identifier(key_token.value)))
            else:
                raise Exception(f"Unexpected token in object: {self.current_token().type}")

            if self.current_token().type == TokenType.COMMA:
                self.advance()
        self.expect(TokenType.RBRACE)
        return ObjectLiteral(properties)

    def _parse_param_list(self):
        self.expect(TokenType.LPAREN)
        params = []
        if self.current_token().type != TokenType.RPAREN:
            if self.current_token().type == TokenType.SPREAD:
                self.advance()
                params.append("..." + self.expect(TokenType.IDENTIFIER).value)
            else:
                params.append(self.expect(TokenType.IDENTIFIER).value)
            while self.current_token().type == TokenType.COMMA:
                self.advance()
                if self.current_token().type == TokenType.SPREAD:
                    self.advance()
                    params.append("..." + self.expect(TokenType.IDENTIFIER).value)
                else:
                    params.append(self.expect(TokenType.IDENTIFIER).value)
        self.expect(TokenType.RPAREN)
        return params

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

        if self.current_token().type in (TokenType.LET, TokenType.CONST, TokenType.VAR):
            init = self.parse_variable_declaration()
        elif self.current_token().type == TokenType.SEMICOLON:
            init = None
            self.advance()
        else:
            init = self.parse_expression_statement()

        if self.current_token().type == TokenType.SEMICOLON:
            test = None
            self.advance()
        else:
            test = self.parse_expression()
            self.expect(TokenType.SEMICOLON)

        if self.current_token().type == TokenType.RPAREN:
            update = None
        else:
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

    def parse_do_while_statement(self):
        self.expect(TokenType.DO)
        body = self.parse_block()
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        test = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.eat_semicolon()
        return DoWhileStatement(body, test)

    def parse_switch_statement(self):
        self.expect(TokenType.SWITCH)
        self.expect(TokenType.LPAREN)
        discriminant = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE)

        cases = []
        while self.current_token().type != TokenType.RBRACE:
            if self.current_token().type == TokenType.CASE:
                self.advance()
                test = self.parse_expression()
                self.expect(TokenType.COLON)
                body = []
                while self.current_token().type not in (TokenType.CASE, TokenType.DEFAULT, TokenType.RBRACE):
                    body.append(self.parse_statement())
                cases.append(SwitchCase(test, body))
            elif self.current_token().type == TokenType.DEFAULT:
                self.advance()
                self.expect(TokenType.COLON)
                body = []
                while self.current_token().type not in (TokenType.CASE, TokenType.DEFAULT, TokenType.RBRACE):
                    body.append(self.parse_statement())
                cases.append(SwitchCase(None, body))

        self.expect(TokenType.RBRACE)
        return SwitchStatement(discriminant, cases)

    def parse_function_declaration(self):
        self.expect(TokenType.FUNCTION)
        name = self.expect(TokenType.IDENTIFIER).value
        params = self._parse_param_list()
        body = self.parse_block()
        return FunctionDeclaration(name, params, body)

    def parse_return_statement(self):
        self.expect(TokenType.RETURN)
        value = None
        if self.current_token().type not in (TokenType.SEMICOLON, TokenType.RBRACE):
            value = self.parse_expression()
        self.eat_semicolon()
        return ReturnStatement(value)
