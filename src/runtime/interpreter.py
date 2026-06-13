import math
from src.runtime.environment import Environment
from src.parser.ast_nodes import (
    Program,
    VariableDeclaration,
    NumberLiteral,
    StringLiteral,
    BooleanLiteral,
    NullLiteral,
    Identifier,
    BinaryExpression,
    AssignmentExpression,
    UpdateExpression,
    IfStatement,
    CallExpression,
    MemberExpression,
    ForStatement,
    WhileStatement,
    FunctionDeclaration,
    ReturnStatement,
    ArrayLiteral,
    SpreadElement,
    ExpressionStatement,
)


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


def js_typeof(val):
    if val is None:
        return "undefined"
    if isinstance(val, bool):
        return "boolean"
    if isinstance(val, (int, float)):
        return "number"
    if isinstance(val, str):
        return "string"
    if isinstance(val, list):
        return "object"
    if callable(val):
        return "function"
    return "object"


def js_to_string(val):
    if val is None:
        return "undefined"
    if val is True:
        return "true"
    if val is False:
        return "false"
    if isinstance(val, float):
        if val == int(val) and not (val != val):  # not NaN
            return str(int(val))
        return str(val)
    if isinstance(val, int):
        return str(val)
    if isinstance(val, str):
        return val
    if isinstance(val, list):
        return ",".join(js_to_string(item) for item in val)
    return str(val)


class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.environment = self.global_env
        self.output = []

    def execute(self, node, env=None):
        if env is not None:
            old_env = self.environment
            self.environment = env
            result = self._exec(node)
            self.environment = old_env
            return result
        return self._exec(node)

    def _exec(self, node):
        if isinstance(node, Program):
            return self.exec_program(node)

        if isinstance(node, VariableDeclaration):
            return self.exec_var_decl(node)

        if isinstance(node, ExpressionStatement):
            return self._exec(node.expression)

        if isinstance(node, NumberLiteral):
            return node.value

        if isinstance(node, StringLiteral):
            return node.value

        if isinstance(node, BooleanLiteral):
            return node.value

        if isinstance(node, NullLiteral):
            return None

        if isinstance(node, Identifier):
            if node.name in ("Math", "console"):
                return node.name
            return self.environment.get(node.name)

        if isinstance(node, BinaryExpression):
            return self.exec_binary(node)

        if isinstance(node, AssignmentExpression):
            return self.exec_assignment(node)

        if isinstance(node, UpdateExpression):
            return self.exec_update(node)

        if isinstance(node, IfStatement):
            return self.exec_if(node)

        if isinstance(node, ForStatement):
            return self.exec_for(node)

        if isinstance(node, WhileStatement):
            return self.exec_while(node)

        if isinstance(node, FunctionDeclaration):
            return self.exec_func_decl(node)

        if isinstance(node, ReturnStatement):
            value = self._exec(node.value) if node.value else None
            raise ReturnSignal(value)

        if isinstance(node, CallExpression):
            return self.exec_call(node)

        if isinstance(node, MemberExpression):
            return self.exec_member(node)

        if isinstance(node, ArrayLiteral):
            return self.exec_array(node)

        raise Exception(f"Unknown node: {type(node).__name__}")

    def exec_program(self, program):
        result = None
        for stmt in program.statements:
            result = self._exec(stmt)
        return result

    def exec_var_decl(self, node):
        value = self._exec(node.value)
        self.environment.define(node.name, value)

    def exec_binary(self, node):
        # Handle logical operators with short-circuit
        if node.operator == "&&":
            left = self._exec(node.left)
            if not left:
                return left
            return self._exec(node.right)
        if node.operator == "||":
            left = self._exec(node.left)
            if left:
                return left
            return self._exec(node.right)
        if node.operator == "!":
            return not self._exec(node.left)

        left = self._exec(node.left)
        right = self._exec(node.right)

        op = node.operator

        # JS-like + coercion: if either side is string, concatenate
        if op == "+":
            if isinstance(left, str) or isinstance(right, str):
                return js_to_string(left) + js_to_string(right)
            return left + right
        if op == "-":
            return left - right
        if op == "*":
            return left * right
        if op == "/":
            if isinstance(left, int) and isinstance(right, int) and left % right == 0:
                return left // right
            return left / right
        if op == "%":
            return left % right
        if op == "**":
            result = left ** right
            if isinstance(result, float) and result == int(result):
                return int(result)
            return result

        if op == "===":
            if type(left) != type(right):
                return False
            return left == right
        if op == "!==":
            if type(left) != type(right):
                return True
            return left != right
        if op == "==":
            return left == right
        if op == "!=":
            return left != right

        if op == "<":
            return left < right
        if op == "<=":
            return left <= right
        if op == ">":
            return left > right
        if op == ">=":
            return left >= right

        raise Exception(f"Unknown operator: {op}")

    def exec_assignment(self, node):
        value = self._exec(node.value)
        if node.operator == "=":
            self.environment.set(node.name, value)
            return value
        if node.operator == "+=":
            current = self.environment.get(node.name)
            if isinstance(current, str) or isinstance(value, str):
                new_val = js_to_string(current) + js_to_string(value)
            else:
                new_val = current + value
            self.environment.set(node.name, new_val)
            return new_val
        if node.operator == "-=":
            current = self.environment.get(node.name)
            new_val = current - value
            self.environment.set(node.name, new_val)
            return new_val

    def exec_update(self, node):
        current = self.environment.get(node.name)
        if node.operator == "++":
            self.environment.set(node.name, current + 1)
            return current  # postfix returns old value

    def exec_if(self, node):
        condition = self._exec(node.condition)
        if condition:
            for stmt in node.then_branch:
                self._exec(stmt)
        elif node.else_branch:
            for stmt in node.else_branch:
                self._exec(stmt)

    def exec_for(self, node):
        loop_env = Environment(self.environment)
        old_env = self.environment
        self.environment = loop_env

        self._exec(node.init)
        while True:
            test = self._exec(node.test)
            if not test:
                break
            for stmt in node.body:
                self._exec(stmt)
            self._exec(node.update)

        self.environment = old_env

    def exec_while(self, node):
        while True:
            test = self._exec(node.test)
            if not test:
                break
            for stmt in node.body:
                self._exec(stmt)

    def exec_func_decl(self, node):
        closure_env = self.environment

        def func(*args):
            func_env = Environment(closure_env)
            for i, param in enumerate(node.params):
                func_env.define(param, args[i] if i < len(args) else None)
            try:
                for stmt in node.body:
                    self.execute(stmt, func_env)
            except ReturnSignal as r:
                return r.value
            return None

        self.environment.define(node.name, func)

    def exec_call(self, node):
        callee = node.callee

        # console.log
        if isinstance(callee, MemberExpression):
            if isinstance(callee.object, Identifier) and callee.object.name == "console" and callee.property == "log":
                args = [self._exec(a) for a in node.arguments]
                line = " ".join(js_to_string(a) for a in args)
                print(line)
                self.output.append(line)
                return None

        # method calls: obj.method(args)
        if isinstance(callee, MemberExpression):
            obj = self._exec(callee.object)
            method_name = callee.property

            args = [self._exec(a) for a in node.arguments]

            # Math methods
            if isinstance(callee.object, Identifier) and callee.object.name == "Math":
                return self.call_math(method_name, args)

            # String methods
            if isinstance(obj, str):
                return self.call_string_method(obj, method_name, args)

            # Array methods
            if isinstance(obj, list):
                return self.call_array_method(obj, method_name, args, callee.object)

            raise Exception(f"Cannot call method {method_name} on {type(obj)}")

        # Regular function call
        func = self._exec(callee)
        args = [self._exec(a) for a in node.arguments]
        return func(*args)

    def call_math(self, method, args):
        if method == "floor":
            return int(math.floor(args[0]))
        if method == "ceil":
            return int(math.ceil(args[0]))
        if method == "round":
            return int(round(args[0]))
        if method == "abs":
            return abs(args[0])
        if method == "sqrt":
            return math.sqrt(args[0])
        if method == "pow":
            result = args[0] ** args[1]
            if isinstance(result, float) and result == int(result):
                return int(result)
            return result
        if method == "max":
            return max(args)
        if method == "min":
            return min(args)
        if method == "random":
            import random
            return random.random()
        raise Exception(f"Unknown Math method: {method}")

    def call_string_method(self, s, method, args):
        if method == "split":
            sep = args[0] if args else ""
            if sep == "":
                return list(s)
            return s.split(sep)
        if method == "join":
            sep = args[0] if args else ","
            return sep.join(js_to_string(item) for item in s)
        if method == "toUpperCase":
            return s.upper()
        if method == "toLowerCase":
            return s.lower()
        if method == "trim":
            return s.strip()
        if method == "includes":
            return args[0] in s
        if method == "indexOf":
            try:
                return s.index(args[0])
            except ValueError:
                return -1
        if method == "startsWith":
            return s.startswith(args[0])
        if method == "endsWith":
            return s.endswith(args[0])
        if method == "substring":
            start = args[0]
            end = args[1] if len(args) > 1 else len(s)
            return s[start:end]
        if method == "slice":
            start = args[0]
            end = args[1] if len(args) > 1 else len(s)
            return s[start:end]
        if method == "replace":
            return s.replace(args[0], args[1], 1)
        if method == "replaceAll":
            return s.replace(args[0], args[1])
        if method == "charAt":
            idx = args[0] if args else 0
            return s[idx] if 0 <= idx < len(s) else ""
        if method == "charCodeAt":
            idx = args[0] if args else 0
            return ord(s[idx]) if 0 <= idx < len(s) else float('nan')
        if method == "repeat":
            return s * args[0]
        if method == "padStart":
            width = args[0]
            fill = args[1] if len(args) > 1 else " "
            return s.rjust(width, fill)
        if method == "padEnd":
            width = args[0]
            fill = args[1] if len(args) > 1 else " "
            return s.ljust(width, fill)
        raise Exception(f"Unknown string method: {method}")

    def call_array_method(self, arr, method, args, obj_node=None):
        if method == "reverse":
            arr.reverse()
            return arr
        if method == "join":
            sep = args[0] if args else ","
            return sep.join(js_to_string(item) for item in arr)
        if method == "push":
            for a in args:
                arr.append(a)
            return len(arr)
        if method == "pop":
            return arr.pop() if arr else None
        if method == "shift":
            return arr.pop(0) if arr else None
        if method == "unshift":
            for a in reversed(args):
                arr.insert(0, a)
            return len(arr)
        if method == "indexOf":
            try:
                return arr.index(args[0])
            except ValueError:
                return -1
        if method == "includes":
            return args[0] in arr
        if method == "slice":
            start = args[0] if args else 0
            end = args[1] if len(args) > 1 else len(arr)
            return arr[start:end]
        if method == "splice":
            start = args[0]
            delete_count = args[1] if len(args) > 1 else len(arr) - start
            removed = arr[start:start + delete_count]
            new_items = args[2:]
            arr[start:start + delete_count] = new_items
            return removed
        if method == "concat":
            result = arr[:]
            for a in args:
                if isinstance(a, list):
                    result.extend(a)
                else:
                    result.append(a)
            return result
        if method == "sort":
            if args and callable(args[0]):
                import functools
                arr.sort(key=functools.cmp_to_key(args[0]))
            else:
                arr.sort(key=lambda x: js_to_string(x))
            return arr
        if method == "map":
            fn = args[0]
            return [fn(item, i, arr) if self._func_arity(fn) >= 2 else fn(item) for i, item in enumerate(arr)]
        if method == "filter":
            fn = args[0]
            return [item for item in arr if fn(item)]
        if method == "reduce":
            fn = args[0]
            acc = args[1] if len(args) > 1 else arr[0]
            start_idx = 0 if len(args) > 1 else 1
            for i in range(start_idx, len(arr)):
                acc = fn(acc, arr[i], i, arr)
            return acc
        if method == "find":
            fn = args[0]
            for item in arr:
                if fn(item):
                    return item
            return None
        if method == "some":
            fn = args[0]
            return any(fn(item) for item in arr)
        if method == "every":
            fn = args[0]
            return all(fn(item) for item in arr)
        if method == "forEach":
            fn = args[0]
            for i, item in enumerate(arr):
                fn(item, i, arr)
            return None
        if method == "length":
            return len(arr)
        raise Exception(f"Unknown array method: {method}")

    def _func_arity(self, fn):
        try:
            import inspect
            return len(inspect.signature(fn).parameters)
        except Exception:
            return 1

    def exec_member(self, node):
        obj = self._exec(node.object)

        if node.computed:
            prop = self._exec(node.property)
            if isinstance(obj, list):
                return obj[prop]
            if isinstance(obj, str):
                return obj[prop]
            if isinstance(obj, dict):
                return obj[prop]

        prop = node.property

        # Math constants
        if obj == "Math":
            if prop == "PI":
                return math.pi
            if prop == "E":
                return math.e

        if isinstance(obj, list):
            if prop == "length":
                return len(obj)

        if isinstance(obj, str):
            if prop == "length":
                return len(obj)

        if isinstance(obj, dict):
            return obj.get(prop)

        raise Exception(f"Cannot access property '{prop}' on {type(obj)}")

    def exec_array(self, node):
        result = []
        for el in node.elements:
            if isinstance(el, SpreadElement):
                iterable = self._exec(el.argument)
                result.extend(iterable)
            else:
                result.append(self._exec(el))
        return result