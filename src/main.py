import sys
import os
from src.lexer.tokenizer import Tokenizer
from src.parser.parser import Parser
from src.runtime.interpreter import Interpreter


def run(code):
    # Handle Windows cmd.exe echo behavior where outer quotes and trailing spaces are piped
    code_stripped = code.strip()
    if len(code_stripped) >= 2:
        first = code_stripped[0]
        last = code_stripped[-1]
        if first == last and first in ('"', "'", "`"):
            code = code_stripped[1:-1]

    tokens = Tokenizer(code).tokenize()
    ast = Parser(tokens).parse()
    interpreter = Interpreter()
    interpreter.execute(ast)


def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.isfile(arg):
            with open(arg, encoding="utf-8") as f:
                code = f.read()
        else:
            code = arg
    else:
        code = sys.stdin.read()

    run(code)


if __name__ == "__main__":
    main()
