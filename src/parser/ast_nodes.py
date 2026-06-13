class Node:
    pass


class Program(Node):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program({self.statements})"


class VariableDeclaration(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"VariableDeclaration({self.name}, {self.value})"


class NumberLiteral(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumberLiteral({self.value})"


class StringLiteral(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"StringLiteral('{self.value}')"


class Identifier(Node):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"
    
class BinaryExpression(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return (
            f"BinaryExpression("
            f"{self.left}, "
            f"'{self.operator}', "
            f"{self.right})"
        )