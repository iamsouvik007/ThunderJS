from src.lexer.tokenizer import Tokenizer
from src.parser.parser import Parser

with open("examples/test.js") as file:
    code = file.read()

tokens = Tokenizer(code).tokenize()

ast = Parser(tokens).parse()

print(ast)