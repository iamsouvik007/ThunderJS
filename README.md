# ⚡ ThunderJS — A JavaScript Interpreter Built in Python

A hand-crafted JavaScript interpreter written from scratch in Python, featuring a complete lexer, recursive descent parser, and tree-walking interpreter. Built for **Thunder Hackathon 2.0**.

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
│   ├── environment.py  # Variable scope management with lexical scoping
│   └── interpreter.py  # Tree-walking interpreter with JS semantics
└── main.py             # CLI entry point
```

### Design

- **Lexer**: Tokenizes JS source into a stream of tokens. Handles multi-character operators (`===`, `!==`, `**`, `=>`, `...`), string escape sequences, single/multi-line comments, template literals, and numeric literals (int/float).

- **Parser**: Recursive descent parser producing an AST. Implements full operator precedence: assignment → ternary → logical OR → logical AND → equality → comparison → additive → multiplicative → exponentiation → unary → postfix → call/member → primary.

- **Interpreter**: Tree-walking evaluator with proper JS semantics including type coercion, scope chaining, closures, and control flow signals (return/break/continue).

## 🔧 Supported JavaScript Features

### Variable Declarations
- `let`, `const`, `var`
- Uninitialized declarations (`let x;`)

### Data Types
- Numbers (integers, floats, `NaN`, `Infinity`)
- Strings (single/double quotes, template literals, escape sequences)
- Booleans (`true`, `false`)
- `null` and `undefined`
- Arrays
- Objects (literals with shorthand, computed keys, methods, spread)

### Operators
- Arithmetic: `+`, `-`, `*`, `/`, `%`, `**`
- Comparison: `===`, `!==`, `==`, `!=`, `<`, `<=`, `>`, `>=`
- Logical: `&&`, `||`, `!`
- Assignment: `=`, `+=`, `-=`, `*=`, `/=`, `%=`
- Update: `++`, `--` (prefix and postfix)
- Ternary: `? :`
- Spread: `...`
- `typeof`

### Control Flow
- `if` / `else if` / `else`
- `for` loops
- `while` loops
- `do...while` loops
- `switch` / `case` / `default` (with fallthrough)
- `break`, `continue`

### Functions
- Function declarations
- Function expressions
- Arrow functions (`=>`)
- Closures with lexical scoping
- Callbacks and higher-order functions
- Rest parameters (`...args`)
- Recursive functions

### Built-in Objects

**Math**: `floor`, `ceil`, `round`, `abs`, `sqrt`, `pow`, `max`, `min`, `random`, `log`, `sin`, `cos`, `tan`, `trunc`, `sign`, `PI`, `E`

**JSON**: `stringify`, `parse`

**Object**: `keys`, `values`, `entries`, `assign`, `freeze`, `create`

**Array** (static): `isArray`, `from`, `of`

**Number** (static): `isInteger`, `isNaN`, `isFinite`, `parseInt`, `parseFloat`

**Date**: `new Date()`, `getTime`, `getFullYear`, `getMonth`, `getDate`, `getHours`, `getMinutes`, `getSeconds`

### Array Methods
`push`, `pop`, `shift`, `unshift`, `slice`, `splice`, `concat`, `includes`, `indexOf`, `lastIndexOf`, `sort`, `reverse`, `join`, `map`, `filter`, `reduce`, `reduceRight`, `find`, `findIndex`, `some`, `every`, `forEach`, `flat`, `flatMap`, `fill`, `at`, `keys`, `values`, `entries`, `toString`

### String Methods
`split`, `join`, `toUpperCase`, `toLowerCase`, `trim`, `trimStart`, `trimEnd`, `includes`, `indexOf`, `lastIndexOf`, `startsWith`, `endsWith`, `substring`, `slice`, `replace`, `replaceAll`, `charAt`, `charCodeAt`, `repeat`, `padStart`, `padEnd`, `concat`, `at`, `toString`, `valueOf`

### Global Functions
`parseInt`, `parseFloat`, `isNaN`, `isFinite`, `Number`, `String`, `Boolean`

### Type Coercion
- String concatenation with `+` operator
- JS-style loose equality (`==`, `!=`)
- Truthiness/falsiness for conditions

### Comments
- Single-line: `//`
- Multi-line: `/* */`
