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


def run_repl():
    print("ThunderJS v1.0")
    print("Interactive JavaScript Shell")
    print("Type 'exit' or 'quit' to quit.")
    print("")

    interpreter = Interpreter()
    buffer = []
    brace_balance = 0
    paren_balance = 0

    while True:
        try:
            prompt = "js > " if not buffer else "...  "
            line = input(prompt)
            if not buffer and line.strip() in ("exit", "quit"):
                break
            
            buffer.append(line)
            
            # Basic counting of braces and parentheses to detect block completion
            for char in line:
                if char == '{':
                    brace_balance += 1
                elif char == '}':
                    brace_balance -= 1
                elif char == '(':
                    paren_balance += 1
                elif char == ')':
                    paren_balance -= 1

            if brace_balance <= 0 and paren_balance <= 0:
                code = "\n".join(buffer)
                buffer = []
                brace_balance = 0
                paren_balance = 0
                if not code.strip():
                    continue

                tokens = Tokenizer(code).tokenize()
                ast = Parser(tokens).parse()
                interpreter.execute(ast)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break
        except Exception as e:
            buffer = []
            brace_balance = 0
            paren_balance = 0
            print(f"Error: {e}")


def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.isfile(arg):
            with open(arg, encoding="utf-8") as f:
                code = f.read()
        else:
            code = arg
        run(code)
    else:
        if sys.stdin.isatty() or os.environ.get("THUNDER_REPL") == "1":
            run_repl()
        else:
            code = sys.stdin.read()
            run(code)


if __name__ == "__main__":
    main()
