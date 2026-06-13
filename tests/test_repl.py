import os
import subprocess
import sys

def test_repl():
    env = os.environ.copy()
    env["THUNDER_REPL"] = "1"

    p = subprocess.Popen(
        [sys.executable, "main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0,
        env=env
    )

    # Test 1: let x = 10;
    p.stdin.write("let x = 10;\n")
    p.stdin.flush()

    # Test 2: console.log(x);
    p.stdin.write("console.log(x);\n")
    p.stdin.flush()

    # Test 3: function add(a, b) {
    #   return a + b;
    # }
    p.stdin.write("function add(a, b) {\n")
    p.stdin.write("return a + b;\n")
    p.stdin.write("}\n")
    p.stdin.flush()

    # Test 4: console.log(add(10, 20));
    p.stdin.write("console.log(add(10, 20));\n")
    p.stdin.flush()

    # Exit REPL
    p.stdin.write("exit\n")
    p.stdin.flush()

    stdout, stderr = p.communicate(timeout=5)

    print("--- REPL Stdout ---")
    print(repr(stdout))
    print("--- REPL Stderr ---")
    print(repr(stderr))

    # Expect the startup messages and the prompts
    assert "ThunderJS v1.0" in stdout, "REPL startup message missing"
    assert "JS" in stdout, "REPL prompt missing"
    assert ("\u276f" in stdout) or (">" in stdout), "REPL prompt symbol missing"
    
    # Expect output from console.log(x) -> 10
    assert "10" in stdout, "REPL failed to output 10"
    
    # Expect output from console.log(add(10, 20)) -> 30
    assert "30" in stdout, "REPL failed to output 30"
    
    # Check stderr is empty
    assert not stderr.strip(), f"REPL stderr is not empty: {stderr}"
    
    print("REPL test PASSED successfully!")

if __name__ == "__main__":
    test_repl()
