import sys
from src.lexer.tokenizer import Tokenizer
from src.parser.parser import Parser
from src.runtime.interpreter import Interpreter


def run(code):
    tokens = Tokenizer(code).tokenize()
    ast = Parser(tokens).parse()
    interpreter = Interpreter()
    interpreter.execute(ast)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        with open(filepath) as f:
            code = f.read()
    else:
        code = sys.stdin.read()

    run(code)
