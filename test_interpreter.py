from src.lexer.tokenizer import Tokenizer
from src.parser.parser import Parser
from src.runtime.interpreter import Interpreter

with open("examples/test.js") as file:
    code = file.read()

tokens = Tokenizer(code).tokenize()

ast = Parser(tokens).parse()

interpreter = Interpreter()

interpreter.execute(ast)

print(interpreter.environment.variables)