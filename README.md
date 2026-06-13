# ThunderJS

A JavaScript interpreter written from scratch in Python. Built for Thunder Hackathon 2.0.

The interpreter takes JavaScript source code as input, tokenizes it, parses it into an abstract syntax tree, and evaluates it — producing the correct output on stdout.

## Overview

ThunderJS is a tree-walking interpreter that executes JavaScript code without relying on any existing JS engine. The entire pipeline — lexing, parsing, and evaluation — is implemented in Python.

**Execution flow:**

```
JavaScript Source → Tokenizer → Tokens → Parser → AST → Interpreter → Output
```

The tokenizer breaks source code into tokens (keywords, operators, literals, etc.). The parser consumes tokens and produces an AST using recursive descent. The interpreter walks the AST and evaluates each node, maintaining variable scopes through a chain of environments.

## Features

### Language Features

- Variable declarations: `let`, `const`, `var`
- Primitive types: numbers, strings, booleans, `null`, `undefined`
- Arithmetic: `+`, `-`, `*`, `/`, `%`, `**`
- Comparison: `===`, `!==`, `==`, `!=`, `<`, `<=`, `>`, `>=`
- Logical operators: `&&`, `||`, `!`
- Assignment: `=`, `+=`, `-=`, `*=`, `/=`, `%=`
- Increment/decrement: `++`, `--` (prefix and postfix)
- Ternary operator: `? :`
- `typeof` operator
- Spread operator: `...`
- Template literals

### Control Flow

- `if` / `else if` / `else`
- `for` loops
- `while` loops
- `do...while` loops
- `switch` / `case` / `default`
- `break`, `continue`

### Functions

- Function declarations
- Function expressions
- Arrow functions
- Closures
- Callbacks and higher-order functions
- Rest parameters
- Recursion

### Data Structures

- Arrays with full method support
- Object literals (shorthand properties, computed keys, methods, spread)

### Built-in Support

- `console.log`
- `Math` object (`floor`, `ceil`, `round`, `abs`, `sqrt`, `pow`, `max`, `min`, `random`, `PI`, `E`, etc.)
- `JSON.stringify`, `JSON.parse`
- `Object.keys`, `Object.values`, `Object.entries`, `Object.assign`
- `Array.isArray`, `Array.from`
- `parseInt`, `parseFloat`, `isNaN`, `isFinite`
- `Number()`, `String()`, `Boolean()` type conversion
- `Date` object (basic support)

### Array Methods

`push`, `pop`, `shift`, `unshift`, `slice`, `splice`, `concat`, `reverse`, `sort`, `join`, `indexOf`, `lastIndexOf`, `includes`, `find`, `findIndex`, `map`, `filter`, `reduce`, `reduceRight`, `some`, `every`, `forEach`, `flat`, `flatMap`, `fill`, `at`

### String Methods

`split`, `toUpperCase`, `toLowerCase`, `trim`, `trimStart`, `trimEnd`, `includes`, `indexOf`, `lastIndexOf`, `startsWith`, `endsWith`, `substring`, `slice`, `replace`, `replaceAll`, `charAt`, `charCodeAt`, `repeat`, `padStart`, `padEnd`, `concat`, `at`

## Project Architecture

```
├── main.py                  # Top-level entry point
├── src/
│   ├── main.py              # Runtime entry point and CLI handling
│   ├── lexer/
│   │   ├── token.py         # Token type definitions
│   │   └── tokenizer.py     # Lexical analysis (source → tokens)
│   ├── parser/
│   │   ├── ast_nodes.py     # AST node class definitions
│   │   └── parser.py        # Recursive descent parser (tokens → AST)
│   ├── runtime/
│   │   ├── interpreter.py   # Tree-walking interpreter (AST → output)
│   │   └── environment.py   # Lexical scope and variable storage
│   └── objects/             # Runtime object type stubs
├── tests/                   # Test case files (.js)
└── examples/                # Example JavaScript files
```

### `src/lexer/`

Handles lexical analysis. The tokenizer scans JavaScript source code character by character and produces a flat list of tokens. It handles multi-character operators (`===`, `!==`, `**`, `=>`), string escape sequences, comments (single-line and multi-line), and numeric literals.

### `src/parser/`

Handles syntax analysis. The parser consumes tokens and builds an AST using recursive descent. Operator precedence is encoded in the call chain:

```
assignment → ternary → logical OR → logical AND → equality
→ comparison → additive → multiplicative → exponentiation
→ unary → postfix → call/member → primary
```

### `src/runtime/`

Handles execution. The interpreter walks the AST and evaluates each node. Variables are stored in `Environment` objects that form a chain for lexical scoping — each scope holds a reference to its parent, enabling closures and block-level variable lookup.

## How It Works

Given this JavaScript input:

```javascript
let x = 10;
let y = 20;
console.log(x + y);
```

1. **Tokenizer** produces: `LET`, `IDENTIFIER(x)`, `ASSIGN`, `NUMBER(10)`, `SEMICOLON`, ...
2. **Parser** builds an AST with `VariableDeclaration` and `ExpressionStatement(CallExpression)` nodes
3. **Interpreter** evaluates the AST:
   - Defines `x = 10` and `y = 20` in the environment
   - Evaluates `x + y` → `30`
   - Calls `console.log(30)` → prints `30` to stdout

## Installation

Requires Python 3.10 or later. No external dependencies.

```bash
git clone <repository-url>
cd Hackathon2
```

## Running the Interpreter

### Method 1 — JavaScript File

```bash
python main.py examples/test.js
```

### Method 2 — Standard Input

```bash
python main.py
# paste JavaScript code, then Ctrl+D (Unix) or Ctrl+Z (Windows)
```

Or pipe input:

```bash
echo 'console.log("hello");' | python main.py
```

### Method 3 — Inline JavaScript String

```bash
python main.py "let x = 42; console.log(x);"
```

### Method 4 — Interactive REPL

If you run `python main.py` directly without arguments and without redirected/piped stdin, the interpreter starts in interactive REPL mode:

```bash
python main.py
```

Example session:

```
==================================================
⚡ ThunderJS v1.0
JavaScript Runtime & Interactive REPL
Built for Thunder Hackathon 2.0
==================================================

Commands:
help   Show available commands
clear  Clear terminal
exit   Exit REPL
quit   Exit REPL

READY

JS ❯ let x = 10;
JS ❯ function add(a, b) {
... ❯ return a + b;
... ❯ }
JS ❯ console.log(add(x, 20));
30
JS ❯ exit
```

### Alternative — Module Execution

```bash
python -m src.main tests/tc1_odd_even.js
```

## Examples

**Odd/Even Check:**

```javascript
let num = 7;
if (num % 2 === 0) {
    console.log(num + " is Even");
} else {
    console.log(num + " is Odd");
}
```

```
7 is Odd
```

**Triangle Pattern:**

```javascript
for (let i = 1; i <= 5; i++) {
    let row = "";
    for (let j = 1; j <= i; j++) {
        row += "*";
    }
    console.log(row);
}
```

```
*
**
***
****
*****
```

**Armstrong Number:**

```javascript
function isArmstrong(num) {
    let temp = num;
    let sum = 0;
    while (temp > 0) {
        let digit = temp % 10;
        sum += digit ** 3;
        temp = Math.floor(temp / 10);
    }
    return sum === num;
}
console.log(isArmstrong(153));
console.log(isArmstrong(123));
```

```
true
false
```

**Array Operations:**

```javascript
let arr = [1, 2, 3, 4, 5];
let reversed = [...arr].reverse();
console.log("Original: " + arr.join(", "));
console.log("Reversed: " + reversed.join(", "));
```

```
Original: 1, 2, 3, 4, 5
Reversed: 5, 4, 3, 2, 1
```

## Testing

Run the provided test cases:

```bash
python main.py tests/tc1_odd_even.js
python main.py tests/tc2_triangle.js
python main.py tests/tc3_armstrong.js
python main.py tests/tc4_array_reverse.js
python main.py tests/tc5_palindrome.js
```

Each test case prints its output to stdout. Compare against expected output to verify correctness.

## Design Decisions

**Recursive descent parser.** Chosen for its straightforward mapping between grammar rules and parsing functions. Each precedence level is a separate method, making the code easy to follow and extend.

**Tree-walking interpreter.** The simplest approach that works — the AST is evaluated directly without compiling to bytecode or any intermediate representation. This keeps the implementation small and easy to debug.

**Environment chain for scoping.** Each scope is an `Environment` object with a pointer to its parent. Variable lookup walks up the chain until a match is found. This naturally handles block scoping, function scoping, and closures without additional machinery.

**JS type coercion in Python.** The `+` operator checks whether either operand is a string and coerces accordingly. Comparison operators, truthiness checks, and equality follow JS semantics where it matters for passing test cases.

## Limitations

This is not a fully standards-compliant JavaScript engine. Notable limitations:

- No `class` syntax
- No destructuring assignments
- No `for...of` / `for...in` loops
- No `try` / `catch` / `throw`
- No `Promise` or async/await
- No regular expressions
- No modules (`import` / `export`)
- No prototype chain or `this` binding
- Template literals do not support `${}` interpolation
- `Date` object has limited method support

The interpreter covers the subset of JavaScript needed for the hackathon test cases and common patterns taught in introductory JS courses.

## Hackathon Submission

- Full source code is in this repository
- No external dependencies — runs with a standard Python installation
- Supports file input, stdin, and command-line string execution
- All five provided test cases produce exact expected output
