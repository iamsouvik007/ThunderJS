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


class UndefinedLiteral(Node):
    pass


class Identifier(Node):
    def __init__(self, name):
        self.name = name


class BinaryExpression(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class UnaryExpression(Node):
    def __init__(self, operator, operand, prefix=True):
        self.operator = operator
        self.operand = operand
        self.prefix = prefix


class AssignmentExpression(Node):
    def __init__(self, target, operator, value):
        self.target = target
        self.operator = operator
        self.value = value


class UpdateExpression(Node):
    def __init__(self, name, operator, prefix=False):
        self.name = name
        self.operator = operator
        self.prefix = prefix


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


class DoWhileStatement(Node):
    def __init__(self, body, test):
        self.body = body
        self.test = test


class SwitchStatement(Node):
    def __init__(self, discriminant, cases):
        self.discriminant = discriminant
        self.cases = cases


class SwitchCase(Node):
    def __init__(self, test, body):
        self.test = test  # None for default
        self.body = body


class BreakStatement(Node):
    pass


class ContinueStatement(Node):
    pass


class FunctionDeclaration(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class FunctionExpression(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class ArrowFunction(Node):
    def __init__(self, params, body):
        self.params = params
        self.body = body


class ReturnStatement(Node):
    def __init__(self, value):
        self.value = value


class ArrayLiteral(Node):
    def __init__(self, elements):
        self.elements = elements


class ObjectLiteral(Node):
    def __init__(self, properties):
        self.properties = properties


class ObjectProperty(Node):
    def __init__(self, key, value, computed=False):
        self.key = key
        self.value = value
        self.computed = computed


class SpreadElement(Node):
    def __init__(self, argument):
        self.argument = argument


class ExpressionStatement(Node):
    def __init__(self, expression):
        self.expression = expression


class ConditionalExpression(Node):
    def __init__(self, test, consequent, alternate):
        self.test = test
        self.consequent = consequent
        self.alternate = alternate


class TypeofExpression(Node):
    def __init__(self, operand):
        self.operand = operand


class NewExpression(Node):
    def __init__(self, callee, arguments):
        self.callee = callee
        self.arguments = arguments