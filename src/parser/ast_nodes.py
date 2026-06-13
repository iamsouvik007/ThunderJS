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


class Identifier(Node):
    def __init__(self, name):
        self.name = name