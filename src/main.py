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

    print(f"{CYAN}==================================================")
    print(f"{lightning}ThunderJS v1.0")
    print("JavaScript Runtime & Interactive REPL")
    print("Built for Thunder Hackathon 2.0")
    print(f"=================================================={RESET}")
    print("")
    print(f"{YELLOW}Commands:{RESET}")
    print(f"{CYAN}help  {RESET} Show available commands")
    print(f"{CYAN}clear {RESET} Clear terminal")
    print(f"{CYAN}exit  {RESET} Exit REPL")
    print(f"{CYAN}quit  {RESET} Exit REPL")
    print("")
    print(f"{GREEN}READY{RESET}")
    print("")

    interpreter = Interpreter()
    buffer = []
    brace_balance = 0
    paren_balance = 0

    import builtins
    original_print = builtins.print

    def repl_print(*args, **kwargs):
        # Format printed strings with green color for success output in REPL
        colored_args = [f"{GREEN}{arg}{RESET}" for arg in args]
        original_print(*colored_args, **kwargs)

    while True:
        try:
            prompt = f"{YELLOW}JS {CYAN}{prompt_symbol}{RESET} " if not buffer else f"{CYAN}... {prompt_symbol}{RESET} "
            line = input(prompt)
            
            # Check commands if buffer is empty
            if not buffer:
                cmd = line.strip()
                if cmd in ("exit", "quit"):
                    break
                if cmd == "clear":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f"{CYAN}Environment cleared{RESET}")
                    continue
                if cmd == "help":
                    print(f"{CYAN}==================================================")
                    print(f"{YELLOW}Command   {CYAN}| {YELLOW}Description")
                    print(f"{CYAN}--------------------------------------------------")
                    print(f"{CYAN}help      {CYAN}| {RESET}Show this help menu")
                    print(f"{CYAN}clear     {CYAN}| {RESET}Clear the terminal screen")
                    print(f"{CYAN}exit/quit {CYAN}| {RESET}Exit the interactive session")
                    print(f"{CYAN}=================================================={RESET}")
                    continue

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
                
                # Monkey-patch builtins.print to print in green during execution
                builtins.print = repl_print
                try:
                    interpreter.execute(ast)
                finally:
                    builtins.print = original_print
                    
        except (KeyboardInterrupt, EOFError):
            print(f"\n{CYAN}Exiting.{RESET}")
            break
        except Exception as e:
            buffer = []
            brace_balance = 0
            paren_balance = 0
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
