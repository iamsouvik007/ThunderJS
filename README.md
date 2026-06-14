<p align="center">
  <img src="ThunderJS.png" alt="ThunderJS Banner" width="100%">
</p>

<h1 align="center">⚡ ThunderJS</h1>

<p align="center">
  <strong>A JavaScript interpreter written from scratch in Python. Built for Thunder Hackathon 2.0.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version" />
  <img src="https://img.shields.io/badge/Tests-25%20%2F%2025%20Passed-brightgreen.svg" alt="Tests Passed" />
  <img src="https://img.shields.io/badge/Dependencies-0-orange.svg" alt="No Dependencies" />
  <img src="https://img.shields.io/badge/Hackathon-Thunder%202.0-blueviolet.svg" alt="Hackathon Project" />
</p>

---

## Overview

ThunderJS is a tree-walking interpreter that executes JavaScript code without relying on any external JavaScript engines. The entire evaluation pipeline — tokenization, parsing, and direct execution — is custom-implemented in Python.

## Installation

```bash
git clone https://github.com/iamsouvik007/ThunderJS.git
cd ThunderJS
```

Requirements:

* Python 3.10+
* No external dependencies

## Quick Start

Run a JavaScript file:

```bash
python main.py examples/test.js
```

Run inline JavaScript:

```bash
python main.py "console.log(1 + 2);"
```

Run JavaScript from standard input:

```bash
echo "console.log(1 + 2);" | python main.py
```

Start the REPL:

```bash
python main.py
```

## Quick Stats

| Metric | Value |
| --- | --- |
| **Language** | Python (3.10+) |
| **Architecture** | Tree-Walking Interpreter |
| **Parser** | Recursive Descent |
| **Tests Passed** | 25 / 25 |
| **Dependencies** | 0 (Standard Library Only) |
| **Input Modes** | File, CLI String, STDIN, Interactive REPL |

## Highlights

- 🚀 **Built completely from scratch**: Custom lexer, parser, and interpreter environment.
- 🌲 **Tree-Walking Interpreter**: Directly executes Abstract Syntax Tree (AST) nodes.
- 📦 **Zero External Dependencies**: Standard library only, keeping it lightweight and fast.
- ⚡ **Multiple Input Modes**: Easy execution via files, inline scripts, piped standard inputs, or the REPL.
- ✅ **Completely Verified**: Fully passes all visible and hidden hackathon test cases.

---

## Execution Flow

```
   JavaScript Source
          │
          ▼
      Tokenizer
          │
          ▼
        Tokens
          │
          ▼
        Parser
          │
          ▼
         AST
          │
          ▼
     Interpreter
          │
          ▼
        Output
```

---

## Features

### Language Features
- [x] **Variable Declarations**: Support for block-scoped `let`, `const`, and `var`.
- [x] **Primitives**: Standard handling of numbers, strings, booleans, `null`, and `undefined`.
- [x] **Operators**: Full arithmetic (`+`, `-`, `*`, `/`, `%`, `**`), logic (`&&`, `||`, `!`), and comparisons (`===`, `!==`, etc.).
- [x] **Assignment**: Compound assignment operators (`=`, `+=`, `-=`, `*=`, `/=`, `%=`).
- [x] **Unary & Update**: Increments/decrements (`++`, `--`) and type checks (`typeof`).
- [x] **Spread**: Support for spread elements (`...`) in array/object initializers and calls.
- [x] **Template Literals**: Basic string literals wrapped in backticks.

### Control Flow
- [x] Conditional branches: `if` / `else if` / `else`
- [x] Switch-case matching: `switch` / `case` / `default`
- [x] Loop statements: `for`, `while`, `do...while`
- [x] Loop controls: `break`, `continue`

### Functions
- [x] Function declarations
- [x] Function expressions
- [x] Arrow functions
- [x] Scope closures and variable mapping
- [x] Callback functions & higher-order functions
- [x] Rest parameters & spread execution
- [x] Full support for recursion

### Arrays
- [x] Array literal syntax and nested lists
- [x] **Static methods**: `Array.isArray`, `Array.from`, `Array.of`
- [x] **Instance methods**:
  - *Mutators*: `push`, `pop`, `shift`, `unshift`, `splice`, `reverse`, `sort`, `fill`
  - *Accessors*: `slice`, `concat`, `join`, `indexOf`, `lastIndexOf`, `includes`, `at`, `toString`
  - *Iterators*: `map`, `filter`, `reduce`, `reduceRight`, `find`, `findIndex`, `some`, `every`, `forEach`, `flat`, `flatMap`
  - *Iterators for keys, values, and entries*: `keys`, `values`, `entries`

### Objects
- [x] Object literal declaration
- [x] Shorthand property initializers
- [x] Computed property keys
- [x] Method definitions
- [x] **Static helper methods**: `Object.keys`, `Object.values`, `Object.entries`, `Object.assign`, `Object.freeze`, `Object.create`

### Built-in Support
- [x] Global logging: `console.log`
- [x] **Math**: `Math` (`floor`, `ceil`, `round`, `abs`, `sqrt`, `pow`, `max`, `min`, `random`, `PI`, `E`)
- [x] **JSON**: `JSON.stringify`, `JSON.parse`
- [x] **Global helpers**: `parseInt`, `parseFloat`, `isNaN`, `isFinite`
- [x] **Type conversion**: `Number()`, `String()`, `Boolean()`
- [x] **Date**: `Date`

---

## Input Modes

### 1. File Input
Executes a JavaScript file directly:
```bash
python main.py examples/test.js
```

### 2. CLI String Input
Executes inline JavaScript code passed as a string:
```bash
python main.py "console.log(1 + 2);"
```

### 3. STDIN Input
Executes JavaScript code piped through standard input:
```bash
echo "console.log(1 + 2);" | python main.py
```

### 4. Interactive REPL
Launches an interactive Read-Eval-Print Loop terminal session with syntax color highlights:
```bash
python main.py
```

---

## Project Architecture

### Component Breakdown

| Component | Description & Responsibility |
| --- | --- |
| **Lexer** | Scans JavaScript source code character-by-character and generates tokens (keywords, literals, operators). Handles comment removal, string escape sequences, and multi-character operators. |
| **Parser** | Performs syntax analysis on the token stream using a *recursive descent* algorithm with precedence climbing. Builds a structured Abstract Syntax Tree (AST). |
| **Runtime** | Traverses the AST in a tree-walking pattern to evaluate expressions, execute statements, and output logs to `stdout`. Delegates array and object prototype actions to decoupled modules. |
| **Environment** | Stores variables, constants, and functions in nested scopes. Connects closures to parent scopes, implementing lexical scoping for correct closures and nested lookups. |

### Directory Structure
```
├── .gitignore
├── README.md
├── ThunderJS.png
├── image.png
├── main.py                  # Top-level entry point
├── requirements.txt         # Project requirements
├── run_all_tests.py         # Test suite runner
├── test_interpreter.py      # Interpreter scratch test script
├── test_parser.py           # Parser scratch test script
├── test_tokenizer.py        # Tokenizer scratch test script
├── examples/
│   └── test.js              # Example JavaScript file
├── src/
│   ├── __init__.py
│   ├── main.py              # Runtime entry point and CLI handling
│   ├── lexer/
│   │   ├── __init__.py
│   │   ├── token.py         # Token type definitions
│   │   └── tokenizer.py     # Lexical analysis (source → tokens)
│   ├── objects/             # Decoupled JS prototype/static handlers
│   │   ├── __init__.py
│   │   ├── js_array.py
│   │   └── js_object.py
│   ├── parser/
│   │   ├── __init__.py
│   │   ├── ast_nodes.py     # AST node class definitions
│   │   └── parser.py        # Recursive descent parser (tokens → AST)
│   ├── runtime/
│   │   ├── __init__.py
│   │   ├── environment.py   # Lexical scope and variable storage
│   │   └── interpreter.py   # Tree-walking interpreter (AST → output)
│   └── utils/               # Shared helpers and interpreter utilities
│       ├── __init__.py
│       └── js_helpers.py
├── tests/                   # Test suite containing JS and Python tests
│   ├── error_tests/         # Syntax and runtime error test cases
│   │   ├── test_call_number.js
│   │   ├── test_function_no_name.js
│   │   ├── test_if_rparen.js
│   │   ├── test_let_eq.js
│   │   ├── test_null_method.js
│   │   ├── test_ref_error.js
│   │   ├── test_unexpected_char.js
│   │   ├── test_unterminated_in_call.js
│   │   └── test_unterminated_string.js
│   ├── debug_fib.js
│   ├── debug_fib2.js
│   ├── hidden_tc1_var.js
│   ├── hidden_tc2_var.js
│   ├── hidden_tc3_var.js
│   ├── hidden_tc4_var.js
│   ├── hidden_tc5_var.js
│   ├── hidden_test1.js
│   ├── hidden_test10.js
│   ├── hidden_test2.js
│   ├── hidden_test3.js
│   ├── hidden_test4.js
│   ├── hidden_test5.js
│   ├── hidden_test6.js
│   ├── hidden_test7.js
│   ├── hidden_test8.js
│   ├── hidden_test9.js
│   ├── judge_arrays.js
│   ├── judge_objects.js
│   ├── judge_recursion.js
│   ├── tc1_odd_even.js
│   ├── tc2_triangle.js
│   ├── tc3_armstrong.js
│   ├── tc4_array_reverse.js
│   ├── tc5_palindrome.js
│   └── test_repl.py         # REPL validation script
```

---

## Testing

The project includes a comprehensive suite of 25 validated test cases. These cover basic language functionality, recursion, complex data structures, and edge cases, ensuring the interpreter remains robust during development.

Run the complete test suite:

```bash
python run_all_tests.py
```

This executes all 25 visible and hidden validation test cases.

Example of running a single test file:

```bash
python main.py tests/tc1_odd_even.js
```

---

## Verification

| Category | Status |
| --- | --- |
| Visible Test Cases | 5 / 5 Passed |
| Hidden Test Cases | 20 / 20 Passed |
| **Total** | **25 / 25 Passed** |

---

## Limitations

ThunderJS focuses on the subset of JavaScript required for hackathon test cases and common algorithmic problems.

Currently unsupported:

* Classes
* Promises
* Async/Await
* ES Modules
* Destructuring Assignment
* for...of / for...in
* try/catch/finally
* Regular Expressions
* Prototype Chain and `this` binding

---

## Hackathon Submission

- **No external dependencies**: Runs with a standard Python 3.10+ installation.
- **Robust test suite**: Tested against all five main hackathon test cases and additional hidden validations.
