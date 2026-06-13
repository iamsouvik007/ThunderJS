<p align="center">
  <img src="ThunderJS.png" alt="ThunderJS Banner" width="600" />
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
- [x] **Variable Declarations**: Support for block-scoped `let`, `const`, and function-scoped `var`.
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
| **Parser** | Performs syntax analysis on the token stream using a recursive descent algorithm with precedence climbing. Builds a structured Abstract Syntax Tree (AST). |
| **Runtime** | Traverses the AST in a tree-walking pattern to evaluate expressions, execute statements, and output logs to `stdout`. Delegates array and object prototype actions to decoupled modules. |
| **Environment** | Stores variables, constants, and functions in nested scopes. Connects closures to parent scopes, implementing lexical scoping for correct closures and nested lookups. |

### Directory Structure
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
│   ├── objects/             # Decoupled JS prototype/static handlers
│   │   ├── js_array.py
│   │   ├── js_object.py
│   │   └── js_function.py
│   └── utils/               # Shared helpers and interpreter utilities
│       └── js_helpers.py
├── tests/                   # Test case files (.js)
└── examples/                # Example JavaScript files
```

---

## Screenshots

### Interactive REPL & Execution Showcase
![REPL Showcase](ThunderJS.png)

---

## Verification

| Category | Status |
| --- | --- |
| Visible Test Cases | 5 / 5 Passed |
| Hidden Test Cases | 20 / 20 Passed |
| **Total** | **25 / 25 Passed** |

---

## Limitations

The interpreter supports the subset of ECMAScript specifications needed to solve common algorithms and course exercises. It does not implement full standards compliance.

| Feature | Status | Alternative / Workaround |
| --- | --- | --- |
| **Classes** | Not Supported | Use factory functions or functional constructors. |
| **Promises** | Not Supported | Use synchronous callback functions. |
| **Modules** | Not Supported | Include definitions within a single executed buffer. |
| **Async/Await** | Not Supported | Rely on synchronous control flow. |
| **Destructuring** | Not Supported | Assign variables using direct index or property keys. |
| **for...of / for...in** | Not Supported | Use a standard `for` loop or `Array.prototype.forEach()`. |
| **try / catch / throw** | Not Supported | Check inputs explicitly for safety. |
| **Regular Expressions** | Not Supported | Use string methods like `split()`, `slice()`, or `indexOf()`. |
| **Prototype Chain / `this`** | Not Supported | Rely on closures and closure environments. |
| **Template Interpolation `${}`**| Not Supported | Use string concatenation (`+`). |

---

## Hackathon Submission

- **No external dependencies**: Runs with a standard Python 3.10+ installation.
- **Robust test suite**: Tested against all five main hackathon test cases and additional hidden validations.
