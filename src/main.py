import sys
import os
import shutil
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
    # Enable ANSI escape code processing in Windows command prompts
    if os.name == 'nt':
        os.system('')

    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"

    # Dynamic fallback to ASCII symbols if the terminal encoding doesn't support Unicode characters
    try:
        encoding = sys.stdout.encoding or 'utf-8'
        "⚡ ❯".encode(encoding)
        lightning = "⚡ "
        prompt_symbol = "❯"
    except UnicodeEncodeError:
        lightning = ""
        prompt_symbol = ">"

    def print_banner():
        width = shutil.get_terminal_size((80, 24)).columns
        sep = "=" * width
        print(f"{CYAN}{sep}")
        print(f"{lightning}ThunderJS v1.0".center(width))
        print("JavaScript Runtime & Interactive REPL".center(width))
        print("Built for Thunder Hackathon 2.0".center(width))
        print(f"{sep}{RESET}")
        print("")
        print("Type JavaScript code below.")
        print("Type 'exit' or 'quit' to leave.")
        print("")
        print(f"{GREEN}READY{RESET}")
        print("")

    print_banner()

    interpreter = Interpreter()
    buffer = []

    def _is_incomplete(code):
        """Try to tokenize+parse code. Return True if it looks incomplete, False otherwise."""
        try:
            tokens = Tokenizer(code).tokenize()
            Parser(tokens).parse()
            return False  # Parsed fine, not incomplete
        except Exception as e:
            msg = str(e)
            # If the parser/tokenizer hit EOF while expecting more input,
            # the code is genuinely incomplete (e.g., unclosed brace/paren).
            if "got TokenType.EOF" in msg or "got EOF" in msg:
                return True
            # Any other error means the code is invalid, not incomplete.
            return False

    while True:
        try:
            prompt = f"{YELLOW}JS {CYAN}{prompt_symbol}{RESET} " if not buffer else f"{CYAN}... {prompt_symbol}{RESET} "
            line = input(prompt)
            
            # Check commands if buffer is empty
            if not buffer:
                cmd = line.strip()
                if cmd in ("exit", "quit"):
                    print("Thanks for using ThunderJS.")
                    break
                if cmd == "clear":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print_banner()
                    continue

            buffer.append(line)
            code = "\n".join(buffer)

            if not code.strip():
                buffer = []
                continue

            # Check if the code looks incomplete (hit EOF while parsing)
            if _is_incomplete(code):
                continue  # Stay in multiline mode

            # Code is complete (or has a real error) — try to execute
            buffer = []
            tokens = Tokenizer(code).tokenize()
            ast = Parser(tokens).parse()
            interpreter.execute(ast)
                    
        except (KeyboardInterrupt, EOFError):
            print("\nThanks for using ThunderJS.")
            break
        except Exception as e:
            buffer = []
            err_msg = str(e)
            if "not defined" in err_msg:
                var_name = err_msg.split("'")[1] if "'" in err_msg else "variable"
                print(f"{RED}ReferenceError: {var_name} is not defined{RESET}")
            else:
                print(f"{RED}Error: {err_msg}{RESET}")


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
