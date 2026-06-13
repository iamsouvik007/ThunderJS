from src.runtime.environment import Environment

from src.parser.ast_nodes import (
    Program,
    VariableDeclaration,
    NumberLiteral,
    StringLiteral,
    Identifier,
    BinaryExpression,
)


class Interpreter:
    def __init__(self):
        self.environment = Environment()

    def execute(self, node):

        if isinstance(node, Program):
            return self.execute_program(node)

        if isinstance(node, VariableDeclaration):
            return self.execute_variable_declaration(node)

        if isinstance(node, NumberLiteral):
            return node.value

        if isinstance(node, Identifier):
            return self.environment.get(
            node.name
        )
        if isinstance(node, BinaryExpression):
            return self.execute_binary(node)

        raise Exception(
            f"Unknown node: {type(node)}"
        )
    

    def execute_program(self, program):
        for statement in program.statements:
            self.execute(statement)

    def execute_variable_declaration(self, node):
        value = self.execute(node.value)

        self.environment.define(
            node.name,
            value
        )

    def execute_binary(self, node):
        left = self.execute(node.left)
        right = self.execute(node.right)

        if node.operator == "+":
            return left + right

        if node.operator == "-":
            return left - right

        if node.operator == "*":
            return left * right

        if node.operator == "/":
            return left / right

        if node.operator == "%":
            return left % right
        
        if node.operator == "===":
            return left == right

        raise Exception(
            f"Unknown operator: {node.operator}"
        )