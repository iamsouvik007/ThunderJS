from src.lexer.tokenizer import Tokenizer

with open("examples/test.js", "r") as file:
    code = file.read()

tokenizer = Tokenizer(code)
tokens = tokenizer.tokenize()

for token in tokens:
    print(token)