class Node:
    pass


class Program(Node):
    def __init__(self, statements):
        self.statements = statements


class VariableDeclaration(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class NumberLiteral(Node):
    def __init__(self, value):
        self.value = value


class StringLiteral(Node):
    def __init__(self, value):
        self.value = value


class BooleanLiteral(Node):
    def __init__(self, value):
        self.value = value


class NullLiteral(Node):
    pass


class Identifier(Node):
    def __init__(self, name):
        self.name = name


class BinaryExpression(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class AssignmentExpression(Node):
    def __init__(self, name, operator, value):
        self.name = name
        self.operator = operator
        self.value = value


class UpdateExpression(Node):
    def __init__(self, name, operator):
        self.name = name
        self.operator = operator


class IfStatement(Node):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class CallExpression(Node):
    def __init__(self, callee, arguments):
        self.callee = callee
        self.arguments = arguments


class MemberExpression(Node):
    def __init__(self, obj, prop, computed=False):
        self.object = obj
        self.property = prop
        self.computed = computed


class ForStatement(Node):
    def __init__(self, init, test, update, body):
        self.init = init
        self.test = test
        self.update = update
        self.body = body


class WhileStatement(Node):
    def __init__(self, test, body):
        self.test = test
        self.body = body


class FunctionDeclaration(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class ReturnStatement(Node):
    def __init__(self, value):
        self.value = value


class ArrayLiteral(Node):
    def __init__(self, elements):
        self.elements = elements


class SpreadElement(Node):
    def __init__(self, argument):
        self.argument = argument


class ExpressionStatement(Node):
    def __init__(self, expression):
        self.expression = expression