# ⚡ ThunderJS — A JavaScript Interpreter Built in Python

A hand-crafted JavaScript interpreter written from scratch in Python. Built for **Thunder Hackathon 2.0**.

## 🚀 How to Run

### Prerequisites
- Python 3.10+

### Run a JavaScript file
```bash
python -m src.main <path-to-js-file>
```

### Run from stdin
```bash
echo 'console.log("Hello World");' | python -m src.main
```

### Run the test cases
```bash
python -m src.main tests/tc1_odd_even.js
python -m src.main tests/tc2_triangle.js
python -m src.main tests/tc3_armstrong.js
python -m src.main tests/tc4_array_reverse.js
python -m src.main tests/tc5_palindrome.js
```

## ✅ Test Case Results

| TC# | Test Case | Status |
|-----|-----------|--------|
| 1 | Odd/Even Checker | ✅ Pass |
| 2 | Triangle Pattern (For Loop) | ✅ Pass |
| 3 | Armstrong Number | ✅ Pass |
| 4 | Array Reverse | ✅ Pass |
| 5 | String Palindrome | ✅ Pass |

## 🏗️ Architecture

```
src/
├── lexer/
│   ├── token.py        # Token types and Token class
│   └── tokenizer.py    # Lexical analysis / scanning
├── parser/
│   ├── ast_nodes.py    # AST node definitions
│   └── parser.py       # Recursive descent parser
├── runtime/
│   ├── environment.py  # Variable scope management
│   └── interpreter.py  # Tree-walking interpreter
└── main.py             # CLI entry point
```

## 🔧 Supported JavaScript Features

- **Variables**: `let`, `const` declarations with assignment
- **Data types**: Numbers (int/float), Strings, Booleans, Arrays, `null`, `undefined`
- **Operators**: `+`, `-`, `*`, `/`, `%`, `**`, `===`, `!==`, `==`, `!=`, `<`, `<=`, `>`, `>=`, `&&`, `||`, `!`
- **Assignment**: `=`, `+=`, `-=`, `++`
- **Control flow**: `if` / `else if` / `else`
- **Loops**: `for`, `while`
- **Functions**: declarations, parameters, return statements, closures
- **Arrays**: literals, spread operator (`...`), `push`, `pop`, `shift`, `unshift`, `reverse`, `join`, `slice`, `splice`, `concat`, `indexOf`, `includes`, `sort`, `map`, `filter`, `reduce`, `find`, `some`, `every`, `forEach`
- **Strings**: `split`, `join`, `toUpperCase`, `toLowerCase`, `trim`, `includes`, `indexOf`, `startsWith`, `endsWith`, `substring`, `slice`, `replace`, `replaceAll`, `charAt`, `repeat`
- **Math**: `Math.floor`, `Math.ceil`, `Math.round`, `Math.abs`, `Math.sqrt`, `Math.pow`, `Math.max`, `Math.min`, `Math.random`, `Math.PI`, `Math.E`
- **Built-in**: `console.log`
- **Comments**: single-line (`//`) and multi-line (`/* */`)
