import math
import random
from src.runtime.environment import Environment
from src.parser.ast_nodes import (
    Program,
    VariableDeclaration,
    NumberLiteral,
    StringLiteral,
    BooleanLiteral,
    NullLiteral,
    UndefinedLiteral,
    Identifier,
    BinaryExpression,
    UnaryExpression,
    AssignmentExpression,
    UpdateExpression,
    IfStatement,
    CallExpression,
    MemberExpression,
    ForStatement,
    WhileStatement,
    DoWhileStatement,
    SwitchStatement,
    BreakStatement,
    ContinueStatement,
    FunctionDeclaration,
    FunctionExpression,
    ArrowFunction,
    ReturnStatement,
    ArrayLiteral,
    ObjectLiteral,
    ObjectProperty,
    SpreadElement,
    ExpressionStatement,
    ConditionalExpression,
    TypeofExpression,
    NewExpression,
)

UNDEFINED = object()


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


class BreakSignal(Exception):
    pass


class ContinueSignal(Exception):
    pass


def js_typeof(val):
    if val is UNDEFINED or val is None:
        if val is UNDEFINED:
            return "undefined"
        return "object"
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
    if isinstance(val, dict):
        return "object"
    return "object"


def js_to_string(val):
    if val is UNDEFINED:
        return "undefined"
    if val is None:
        return "null"
    if val is True:
        return "true"
    if val is False:
        return "false"
    if isinstance(val, float):
        if val != val:
            return "NaN"
        if val == float('inf'):
            return "Infinity"
        if val == float('-inf'):
            return "-Infinity"
        if val == int(val):
            return str(int(val))
        return str(val)
    if isinstance(val, int):
        return str(val)
    if isinstance(val, str):
        return val
    if isinstance(val, list):
        return ",".join(js_to_string(item) for item in val)
    if isinstance(val, dict):
        return "[object Object]"
    if callable(val):
        return "function"
    return str(val)


def js_to_number(val):
    if val is UNDEFINED:
        return float('nan')
    if val is None:
        return 0
    if val is True:
        return 1
    if val is False:
        return 0
    if isinstance(val, (int, float)):
        return val
    if isinstance(val, str):
        s = val.strip()
        if s == "":
            return 0
        try:
            if '.' in s:
                return float(s)
            return int(s)
        except ValueError:
            return float('nan')
    return float('nan')


def js_to_boolean(val):
    if val is UNDEFINED or val is None:
        return False
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        if val != val:  # NaN
            return False
        return val != 0
    if isinstance(val, str):
        return len(val) > 0
    return True


def js_loose_equal(a, b):
    if type(a) == type(b):
        return a == b
    if a is None and b is UNDEFINED:
        return True
    if a is UNDEFINED and b is None:
        return True
    if a is None or b is None or a is UNDEFINED or b is UNDEFINED:
        return False
    if isinstance(a, (int, float)) and isinstance(b, str):
        return a == js_to_number(b)
    if isinstance(a, str) and isinstance(b, (int, float)):
        return js_to_number(a) == b
    if isinstance(a, bool):
        return js_loose_equal(js_to_number(a), b)
    if isinstance(b, bool):
        return js_loose_equal(a, js_to_number(b))
    return a == b


class JSDate:
    def __init__(self, *args):
        import datetime
        if not args:
            self.dt = datetime.datetime.now()
        elif len(args) == 1 and isinstance(args[0], str):
            self.dt = datetime.datetime.fromisoformat(args[0].replace('Z', '+00:00'))
        elif len(args) == 1 and isinstance(args[0], (int, float)):
            self.dt = datetime.datetime.fromtimestamp(args[0] / 1000)
        else:
            parts = list(args) + [1, 0, 0, 0, 0]
            y, m, d = int(parts[0]), int(parts[1]) + 1, int(parts[2])
            h, mi, s = int(parts[3]), int(parts[4]), int(parts[5])
            self.dt = datetime.datetime(y, m, d, h, mi, s)

    def getTime(self):
        return int(self.dt.timestamp() * 1000)

    def getFullYear(self):
        return self.dt.year

    def getMonth(self):
        return self.dt.month - 1

    def getDate(self):
        return self.dt.day

    def getDay(self):
        return self.dt.weekday()

    def getHours(self):
        return self.dt.hour

    def getMinutes(self):
        return self.dt.minute

    def getSeconds(self):
        return self.dt.second

    def getMilliseconds(self):
        return self.dt.microsecond // 1000

    def toISOString(self):
        return self.dt.strftime('%Y-%m-%dT%H:%M:%S.') + f"{self.dt.microsecond // 1000:03d}Z"

    def toString(self):
        return str(self.dt)

    def toLocaleDateString(self):
        return self.dt.strftime('%m/%d/%Y')

    def toDateString(self):
        return self.dt.strftime('%a %b %d %Y')


class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.environment = self.global_env
        self.output = []
        self._setup_globals()

    def _setup_globals(self):
        self.global_env.define("undefined", UNDEFINED)
        self.global_env.define("null", None)
        self.global_env.define("NaN", float('nan'))
        self.global_env.define("Infinity", float('inf'))

        self.global_env.define("parseInt", lambda s, r=10: self._parse_int(s, r))
        self.global_env.define("parseFloat", lambda s: self._parse_float(s))
        self.global_env.define("isNaN", lambda v: v != v if isinstance(v, float) else js_to_number(v) != js_to_number(v))
        self.global_env.define("isFinite", lambda v: isinstance(v, (int, float)) and v == v and v != float('inf') and v != float('-inf'))

        self.global_env.define("Number", lambda v=0: js_to_number(v))
        self.global_env.define("String", lambda v="": js_to_string(v))
        self.global_env.define("Boolean", lambda v=False: js_to_boolean(v))
        self.global_env.define("Array", self._builtin_array)
        self.global_env.define("Object", self._builtin_object)

        self.global_env.define("JSON", "JSON")

    def _parse_int(self, s, radix=10):
        try:
            s = js_to_string(s).strip()
            if radix == 16 or s.startswith('0x') or s.startswith('0X'):
                return int(s, 16)
            num_str = ""
            for c in s:
                if c.isdigit() or (not num_str and c in '+-'):
                    num_str += c
                else:
                    break
            return int(num_str) if num_str else float('nan')
        except (ValueError, TypeError):
            return float('nan')

    def _parse_float(self, s):
        try:
            s = js_to_string(s).strip()
            num_str = ""
            has_dot = False
            for c in s:
                if c.isdigit():
                    num_str += c
                elif c == '.' and not has_dot:
                    has_dot = True
                    num_str += c
                elif not num_str and c in '+-':
                    num_str += c
                else:
                    break
            return float(num_str) if num_str else float('nan')
        except (ValueError, TypeError):
            return float('nan')

    def _builtin_array(self, *args):
        if len(args) == 1 and isinstance(args[0], int):
            return [UNDEFINED] * args[0]
        return list(args)

    def _builtin_object(self, *args):
        return {}

    def execute(self, node, env=None):
        if env is not None:
            old_env = self.environment
            self.environment = env
            try:
                result = self._exec(node)
            finally:
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

        if isinstance(node, UndefinedLiteral):
            return UNDEFINED

        if isinstance(node, Identifier):
            if node.name in ("Math", "console", "JSON", "Date"):
                return node.name
            return self.environment.get(node.name)

        if isinstance(node, BinaryExpression):
            return self.exec_binary(node)

        if isinstance(node, UnaryExpression):
            return self.exec_unary(node)

        if isinstance(node, AssignmentExpression):
            return self.exec_assignment(node)

        if isinstance(node, UpdateExpression):
            return self.exec_update(node)

        if isinstance(node, ConditionalExpression):
            return self.exec_ternary(node)

        if isinstance(node, IfStatement):
            return self.exec_if(node)

        if isinstance(node, ForStatement):
            return self.exec_for(node)

        if isinstance(node, WhileStatement):
            return self.exec_while(node)

        if isinstance(node, DoWhileStatement):
            return self.exec_do_while(node)

        if isinstance(node, SwitchStatement):
            return self.exec_switch(node)

        if isinstance(node, BreakStatement):
            raise BreakSignal()

        if isinstance(node, ContinueStatement):
            raise ContinueSignal()

        if isinstance(node, FunctionDeclaration):
            return self.exec_func_decl(node)

        if isinstance(node, FunctionExpression):
            return self.make_function(node.name, node.params, node.body)

        if isinstance(node, ArrowFunction):
            return self.make_arrow(node.params, node.body)

        if isinstance(node, ReturnStatement):
            value = self._exec(node.value) if node.value else UNDEFINED
            raise ReturnSignal(value)

        if isinstance(node, CallExpression):
            return self.exec_call(node)

        if isinstance(node, NewExpression):
            return self.exec_new(node)

        if isinstance(node, MemberExpression):
            return self.exec_member(node)

        if isinstance(node, ArrayLiteral):
            return self.exec_array(node)

        if isinstance(node, ObjectLiteral):
            return self.exec_object(node)

        if isinstance(node, TypeofExpression):
            return self.exec_typeof(node)

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
        if node.operator == "&&":
            left = self._exec(node.left)
            if not js_to_boolean(left):
                return left
            return self._exec(node.right)
        if node.operator == "||":
            left = self._exec(node.left)
            if js_to_boolean(left):
                return left
            return self._exec(node.right)

        left = self._exec(node.left)
        right = self._exec(node.right)
        op = node.operator

        if op == "+":
            if isinstance(left, str) or isinstance(right, str):
                return js_to_string(left) + js_to_string(right)
            l = js_to_number(left) if not isinstance(left, (int, float)) else left
            r = js_to_number(right) if not isinstance(right, (int, float)) else right
            return l + r
        if op == "-":
            return js_to_number(left) - js_to_number(right) if not (isinstance(left, (int, float)) and isinstance(right, (int, float))) else left - right
        if op == "*":
            return js_to_number(left) * js_to_number(right) if not (isinstance(left, (int, float)) and isinstance(right, (int, float))) else left * right
        if op == "/":
            l = left if isinstance(left, (int, float)) else js_to_number(left)
            r = right if isinstance(right, (int, float)) else js_to_number(right)
            if r == 0:
                if l == 0:
                    return float('nan')
                return float('inf') if l > 0 else float('-inf')
            result = l / r
            if isinstance(result, float) and result == int(result) and abs(result) < 2**53:
                return int(result)
            return result
        if op == "%":
            l = left if isinstance(left, (int, float)) else js_to_number(left)
            r = right if isinstance(right, (int, float)) else js_to_number(right)
            if r == 0:
                return float('nan')
            return l % r
        if op == "**":
            l = left if isinstance(left, (int, float)) else js_to_number(left)
            r = right if isinstance(right, (int, float)) else js_to_number(right)
            result = l ** r
            if isinstance(result, float) and result == int(result) and abs(result) < 2**53:
                return int(result)
            if isinstance(result, complex):
                return float('nan')
            return result

        if op == "===":
            return self._strict_equal(left, right)
        if op == "!==":
            return not self._strict_equal(left, right)
        if op == "==":
            return js_loose_equal(left, right)
        if op == "!=":
            return not js_loose_equal(left, right)

        if op == "<":
            return left < right
        if op == "<=":
            return left <= right
        if op == ">":
            return left > right
        if op == ">=":
            return left >= right

        raise Exception(f"Unknown operator: {op}")

    def _strict_equal(self, left, right):
        if left is UNDEFINED and right is UNDEFINED:
            return True
        if left is None and right is None:
            return True
        if (left is UNDEFINED or left is None) != (right is UNDEFINED or right is None):
            if left is UNDEFINED and right is None:
                return False
            if left is None and right is UNDEFINED:
                return False
        if type(left) != type(right):
            return False
        if isinstance(left, float) and left != left and isinstance(right, float) and right != right:
            return False
        return left == right

    def exec_unary(self, node):
        if node.operator == "!":
            return not js_to_boolean(self._exec(node.operand))
        if node.operator == "-":
            val = self._exec(node.operand)
            return -js_to_number(val) if not isinstance(val, (int, float)) else -val
        if node.operator == "+":
            val = self._exec(node.operand)
            return js_to_number(val)
        raise Exception(f"Unknown unary operator: {node.operator}")

    def exec_assignment(self, node):
        value = self._exec(node.value)
        target = node.target

        if isinstance(target, Identifier):
            name = target.name
            if node.operator == "=":
                self.environment.set(name, value)
                return value
            current = self.environment.get(name)
            new_val = self._apply_compound_assign(current, node.operator, value)
            self.environment.set(name, new_val)
            return new_val

        if isinstance(target, MemberExpression):
            obj = self._exec(target.object)
            if target.computed:
                prop = self._exec(target.property)
            else:
                prop = target.property

            if node.operator == "=":
                if isinstance(obj, list):
                    obj[prop] = value
                elif isinstance(obj, dict):
                    obj[prop] = value
                return value
            else:
                if isinstance(obj, list):
                    current = obj[prop]
                elif isinstance(obj, dict):
                    current = obj.get(prop)
                else:
                    current = 0
                new_val = self._apply_compound_assign(current, node.operator, value)
                if isinstance(obj, list):
                    obj[prop] = new_val
                elif isinstance(obj, dict):
                    obj[prop] = new_val
                return new_val

        raise Exception(f"Invalid assignment target: {type(target).__name__}")

    def _apply_compound_assign(self, current, operator, value):
        if operator == "+=":
            if isinstance(current, str) or isinstance(value, str):
                return js_to_string(current) + js_to_string(value)
            return current + value
        if operator == "-=":
            return current - value
        if operator == "*=":
            return current * value
        if operator == "/=":
            if value == 0:
                return float('inf') if current > 0 else float('-inf') if current < 0 else float('nan')
            result = current / value
            if isinstance(result, float) and result == int(result):
                return int(result)
            return result
        if operator == "%=":
            return current % value
        raise Exception(f"Unknown compound operator: {operator}")

    def exec_update(self, node):
        name = node.name
        current = self.environment.get(name)
        if node.operator == "++":
            self.environment.set(name, current + 1)
            return current + 1 if node.prefix else current
        if node.operator == "--":
            self.environment.set(name, current - 1)
            return current - 1 if node.prefix else current

    def exec_ternary(self, node):
        test = self._exec(node.test)
        if js_to_boolean(test):
            return self._exec(node.consequent)
        return self._exec(node.alternate)

    def exec_if(self, node):
        condition = self._exec(node.condition)
        if js_to_boolean(condition):
            for stmt in node.then_branch:
                self._exec(stmt)
        elif node.else_branch:
            for stmt in node.else_branch:
                self._exec(stmt)

    def exec_for(self, node):
        loop_env = Environment(self.environment)
        old_env = self.environment
        self.environment = loop_env

        if node.init:
            self._exec(node.init)
        try:
            while True:
                if node.test:
                    test = self._exec(node.test)
                    if not js_to_boolean(test):
                        break
                try:
                    for stmt in node.body:
                        self._exec(stmt)
                except ContinueSignal:
                    pass
                except BreakSignal:
                    break
                if node.update:
                    self._exec(node.update)
        finally:
            self.environment = old_env

    def exec_while(self, node):
        while True:
            test = self._exec(node.test)
            if not js_to_boolean(test):
                break
            try:
                for stmt in node.body:
                    self._exec(stmt)
            except ContinueSignal:
                continue
            except BreakSignal:
                break

    def exec_do_while(self, node):
        while True:
            try:
                for stmt in node.body:
                    self._exec(stmt)
            except ContinueSignal:
                pass
            except BreakSignal:
                break
            test = self._exec(node.test)
            if not js_to_boolean(test):
                break

    def exec_switch(self, node):
        disc = self._exec(node.discriminant)
        matched = False
        try:
            for case in node.cases:
                if not matched:
                    if case.test is None:
                        matched = True
                    else:
                        case_val = self._exec(case.test)
                        if self._strict_equal(disc, case_val):
                            matched = True
                if matched:
                    for stmt in case.body:
                        self._exec(stmt)
        except BreakSignal:
            pass

    def exec_func_decl(self, node):
        func = self.make_function(node.name, node.params, node.body)
        self.environment.define(node.name, func)

    def make_function(self, name, params, body):
        closure_env = self.environment

        def func(*args):
            func_env = Environment(closure_env)
            for i, param in enumerate(params):
                if param.startswith("..."):
                    rest_name = param[3:]
                    func_env.define(rest_name, list(args[i:]))
                    break
                func_env.define(param, args[i] if i < len(args) else UNDEFINED)
            try:
                for stmt in body:
                    self.execute(stmt, func_env)
            except ReturnSignal as r:
                return r.value
            return UNDEFINED

        if name:
            func.__name__ = name
        return func

    def make_arrow(self, params, body):
        closure_env = self.environment

        if isinstance(body, list):
            def func(*args):
                func_env = Environment(closure_env)
                for i, param in enumerate(params):
                    if param.startswith("..."):
                        rest_name = param[3:]
                        func_env.define(rest_name, list(args[i:]))
                        break
                    func_env.define(param, args[i] if i < len(args) else UNDEFINED)
                try:
                    for stmt in body:
                        self.execute(stmt, func_env)
                except ReturnSignal as r:
                    return r.value
                return UNDEFINED
        else:
            def func(*args):
                func_env = Environment(closure_env)
                for i, param in enumerate(params):
                    if param.startswith("..."):
                        rest_name = param[3:]
                        func_env.define(rest_name, list(args[i:]))
                        break
                    func_env.define(param, args[i] if i < len(args) else UNDEFINED)
                return self.execute(body, func_env)

        return func

    def exec_call(self, node):
        callee = node.callee

        # console.log
        if isinstance(callee, MemberExpression) and isinstance(callee.object, Identifier):
            obj_name = callee.object.name
            if obj_name == "console" and callee.property == "log":
                args = self._eval_call_args(node.arguments)
                line = " ".join(js_to_string(a) for a in args)
                print(line)
                self.output.append(line)
                return UNDEFINED

            if obj_name == "Math":
                args = self._eval_call_args(node.arguments)
                return self.call_math(callee.property, args)

            if obj_name == "JSON":
                args = self._eval_call_args(node.arguments)
                return self.call_json(callee.property, args)

            if obj_name == "Date":
                if callee.property == "now":
                    import time
                    return int(time.time() * 1000)

            if obj_name == "Object":
                args = self._eval_call_args(node.arguments)
                return self.call_object_static(callee.property, args)

            if obj_name == "Array":
                args = self._eval_call_args(node.arguments)
                return self.call_array_static(callee.property, args)

            if obj_name == "Number":
                args = self._eval_call_args(node.arguments)
                return self.call_number_static(callee.property, args)

        # method calls on evaluated objects
        if isinstance(callee, MemberExpression):
            obj = self._exec(callee.object)
            method_name = callee.property if not callee.computed else self._exec(callee.property)

            args = self._eval_call_args(node.arguments)

            if isinstance(obj, str):
                if obj == "Math":
                    return self.call_math(method_name, args)
                if obj == "JSON":
                    return self.call_json(method_name, args)
                return self.call_string_method(obj, method_name, args)

            if isinstance(obj, list):
                return self.call_array_method(obj, method_name, args)

            if isinstance(obj, dict):
                method = obj.get(method_name)
                if callable(method):
                    return method(*args)
                raise Exception(f"'{method_name}' is not a function")

            if isinstance(obj, JSDate):
                method = getattr(obj, method_name, None)
                if method and callable(method):
                    return method(*args)

            if callable(obj):
                return obj(*args)

            raise Exception(f"Cannot call method {method_name} on {type(obj)}")

        # Regular function call
        func = self._exec(callee)
        args = self._eval_call_args(node.arguments)
        if not callable(func):
            raise Exception(f"{js_to_string(func)} is not a function")
        return func(*args)

    def _eval_call_args(self, arg_nodes):
        args = []
        for a in arg_nodes:
            if isinstance(a, SpreadElement):
                iterable = self._exec(a.argument)
                args.extend(iterable)
            else:
                args.append(self._exec(a))
        return args

    def exec_new(self, node):
        callee = node.callee
        args = self._eval_call_args(node.arguments)

        if isinstance(callee, Identifier) and callee.name == "Date":
            return JSDate(*args)

        if isinstance(callee, Identifier) and callee.name == "Array":
            return self._builtin_array(*args)

        if isinstance(callee, Identifier) and callee.name == "Object":
            return {}

        func = self._exec(callee)
        if callable(func):
            obj = {}
            result = func(*args)
            if isinstance(result, dict):
                return result
            return obj
        raise Exception("Not a constructor")

    def call_math(self, method, args):
        if method == "floor":
            return int(math.floor(args[0]))
        if method == "ceil":
            return int(math.ceil(args[0]))
        if method == "round":
            v = args[0]
            return int(math.floor(v + 0.5))
        if method == "abs":
            r = abs(args[0])
            return int(r) if isinstance(r, float) and r == int(r) else r
        if method == "sqrt":
            r = math.sqrt(args[0])
            return int(r) if r == int(r) else r
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
            return random.random()
        if method == "log":
            return math.log(args[0])
        if method == "log2":
            return math.log2(args[0])
        if method == "log10":
            return math.log10(args[0])
        if method == "sin":
            return math.sin(args[0])
        if method == "cos":
            return math.cos(args[0])
        if method == "tan":
            return math.tan(args[0])
        if method == "trunc":
            return int(args[0])
        if method == "sign":
            v = args[0]
            if v > 0:
                return 1
            if v < 0:
                return -1
            return 0
        raise Exception(f"Unknown Math method: {method}")

    def call_json(self, method, args):
        import json
        if method == "stringify":
            obj = args[0]
            return json.dumps(self._to_json_serializable(obj), separators=(",", ":"))
        if method == "parse":
            return json.loads(args[0])
        raise Exception(f"Unknown JSON method: {method}")

    def _to_json_serializable(self, val):
        if val is UNDEFINED:
            return None
        if val is None:
            return None
        if isinstance(val, bool):
            return val
        if isinstance(val, (int, float)):
            return val
        if isinstance(val, str):
            return val
        if isinstance(val, list):
            return [self._to_json_serializable(item) for item in val]
        if isinstance(val, dict):
            return {k: self._to_json_serializable(v) for k, v in val.items()}
        return str(val)

    def call_object_static(self, method, args):
        if method == "keys":
            obj = args[0] if args else {}
            return list(obj.keys()) if isinstance(obj, dict) else []
        if method == "values":
            obj = args[0] if args else {}
            return list(obj.values()) if isinstance(obj, dict) else []
        if method == "entries":
            obj = args[0] if args else {}
            return [[k, v] for k, v in obj.items()] if isinstance(obj, dict) else []
        if method == "assign":
            target = args[0] if args else {}
            for src in args[1:]:
                if isinstance(src, dict):
                    target.update(src)
            return target
        if method == "freeze":
            return args[0] if args else {}
        if method == "create":
            return {}
        raise Exception(f"Unknown Object method: {method}")

    def call_array_static(self, method, args):
        if method == "isArray":
            return isinstance(args[0], list) if args else False
        if method == "from":
            src = args[0] if args else []
            if isinstance(src, str):
                result = list(src)
            elif isinstance(src, list):
                result = src[:]
            else:
                result = list(src)
            if len(args) > 1 and callable(args[1]):
                result = [args[1](item, i) for i, item in enumerate(result)]
            return result
        if method == "of":
            return list(args)
        raise Exception(f"Unknown Array static method: {method}")

    def call_number_static(self, method, args):
        if method == "isInteger":
            v = args[0] if args else UNDEFINED
            return isinstance(v, int) or (isinstance(v, float) and v == int(v) and v == v)
        if method == "isNaN":
            v = args[0] if args else UNDEFINED
            return isinstance(v, float) and v != v
        if method == "isFinite":
            v = args[0] if args else UNDEFINED
            return isinstance(v, (int, float)) and v == v and v != float('inf') and v != float('-inf')
        if method == "parseInt":
            return self._parse_int(args[0] if args else "", args[1] if len(args) > 1 else 10)
        if method == "parseFloat":
            return self._parse_float(args[0] if args else "")
        raise Exception(f"Unknown Number method: {method}")

    def call_string_method(self, s, method, args):
        if method == "split":
            sep = args[0] if args else UNDEFINED
            if sep is UNDEFINED:
                return [s]
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
        if method == "trimStart" or method == "trimLeft":
            return s.lstrip()
        if method == "trimEnd" or method == "trimRight":
            return s.rstrip()
        if method == "includes":
            return args[0] in s if args else False
        if method == "indexOf":
            search = args[0] if args else ""
            start = args[1] if len(args) > 1 else 0
            try:
                return s.index(search, start)
            except ValueError:
                return -1
        if method == "lastIndexOf":
            search = args[0] if args else ""
            try:
                return s.rindex(search)
            except ValueError:
                return -1
        if method == "startsWith":
            return s.startswith(args[0]) if args else False
        if method == "endsWith":
            return s.endswith(args[0]) if args else False
        if method == "substring":
            start = int(args[0]) if args else 0
            end = int(args[1]) if len(args) > 1 else len(s)
            if start < 0:
                start = 0
            if end < 0:
                end = 0
            if start > end:
                start, end = end, start
            return s[start:end]
        if method == "slice":
            start = int(args[0]) if args else 0
            end = int(args[1]) if len(args) > 1 else len(s)
            return s[start:end]
        if method == "replace":
            return s.replace(args[0], args[1], 1) if len(args) >= 2 else s
        if method == "replaceAll":
            return s.replace(args[0], args[1]) if len(args) >= 2 else s
        if method == "charAt":
            idx = int(args[0]) if args else 0
            return s[idx] if 0 <= idx < len(s) else ""
        if method == "charCodeAt":
            idx = int(args[0]) if args else 0
            return ord(s[idx]) if 0 <= idx < len(s) else float('nan')
        if method == "repeat":
            return s * int(args[0]) if args else ""
        if method == "padStart":
            width = int(args[0]) if args else 0
            fill = args[1] if len(args) > 1 else " "
            result = s
            while len(result) < width:
                result = fill + result
            return result[:width] if len(result) > width else result
        if method == "padEnd":
            width = int(args[0]) if args else 0
            fill = args[1] if len(args) > 1 else " "
            result = s
            while len(result) < width:
                result = result + fill
            return result[:width] if len(result) > width else result
        if method == "concat":
            result = s
            for a in args:
                result += js_to_string(a)
            return result
        if method == "match":
            return None
        if method == "search":
            return -1
        if method == "at":
            idx = int(args[0]) if args else 0
            if idx < 0:
                idx = len(s) + idx
            return s[idx] if 0 <= idx < len(s) else UNDEFINED
        if method == "toString":
            return s
        if method == "valueOf":
            return s
        raise Exception(f"Unknown string method: {method}")

    def call_array_method(self, arr, method, args):
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
            return arr.pop() if arr else UNDEFINED
        if method == "shift":
            return arr.pop(0) if arr else UNDEFINED
        if method == "unshift":
            for a in reversed(args):
                arr.insert(0, a)
            return len(arr)
        if method == "indexOf":
            search = args[0] if args else UNDEFINED
            start = int(args[1]) if len(args) > 1 else 0
            for i in range(start, len(arr)):
                if self._strict_equal(arr[i], search):
                    return i
            return -1
        if method == "lastIndexOf":
            search = args[0] if args else UNDEFINED
            for i in range(len(arr) - 1, -1, -1):
                if self._strict_equal(arr[i], search):
                    return i
            return -1
        if method == "includes":
            search = args[0] if args else UNDEFINED
            return any(self._strict_equal(item, search) for item in arr)
        if method == "slice":
            start = int(args[0]) if args else 0
            end = int(args[1]) if len(args) > 1 else len(arr)
            return arr[start:end]
        if method == "splice":
            start = int(args[0])
            if start < 0:
                start = max(len(arr) + start, 0)
            delete_count = int(args[1]) if len(args) > 1 else len(arr) - start
            removed = arr[start:start + delete_count]
            new_items = list(args[2:])
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
                arr.sort(key=functools.cmp_to_key(lambda a, b: int(args[0](a, b))))
            else:
                arr.sort(key=lambda x: js_to_string(x))
            return arr
        if method == "map":
            fn = args[0]
            result = []
            for i, item in enumerate(arr):
                try:
                    result.append(fn(item, i, arr))
                except TypeError:
                    result.append(fn(item))
            return result
        if method == "filter":
            fn = args[0]
            result = []
            for i, item in enumerate(arr):
                try:
                    val = fn(item, i, arr)
                except TypeError:
                    val = fn(item)
                if js_to_boolean(val):
                    result.append(item)
            return result
        if method == "reduce":
            fn = args[0]
            if len(args) > 1:
                acc = args[1]
                start_idx = 0
            else:
                acc = arr[0]
                start_idx = 1
            for i in range(start_idx, len(arr)):
                try:
                    acc = fn(acc, arr[i], i, arr)
                except TypeError:
                    acc = fn(acc, arr[i])
            return acc
        if method == "reduceRight":
            fn = args[0]
            if len(args) > 1:
                acc = args[1]
                start_idx = len(arr) - 1
            else:
                acc = arr[-1]
                start_idx = len(arr) - 2
            for i in range(start_idx, -1, -1):
                try:
                    acc = fn(acc, arr[i], i, arr)
                except TypeError:
                    acc = fn(acc, arr[i])
            return acc
        if method == "find":
            fn = args[0]
            for i, item in enumerate(arr):
                try:
                    val = fn(item, i, arr)
                except TypeError:
                    val = fn(item)
                if js_to_boolean(val):
                    return item
            return UNDEFINED
        if method == "findIndex":
            fn = args[0]
            for i, item in enumerate(arr):
                try:
                    val = fn(item, i, arr)
                except TypeError:
                    val = fn(item)
                if js_to_boolean(val):
                    return i
            return -1
        if method == "some":
            fn = args[0]
            for i, item in enumerate(arr):
                try:
                    val = fn(item, i, arr)
                except TypeError:
                    val = fn(item)
                if js_to_boolean(val):
                    return True
            return False
        if method == "every":
            fn = args[0]
            for i, item in enumerate(arr):
                try:
                    val = fn(item, i, arr)
                except TypeError:
                    val = fn(item)
                if not js_to_boolean(val):
                    return False
            return True
        if method == "forEach":
            fn = args[0]
            for i, item in enumerate(arr):
                try:
                    fn(item, i, arr)
                except TypeError:
                    fn(item)
            return UNDEFINED
        if method == "flat":
            depth = int(args[0]) if args else 1
            return self._flatten(arr, depth)
        if method == "flatMap":
            fn = args[0]
            mapped = []
            for i, item in enumerate(arr):
                try:
                    result = fn(item, i, arr)
                except TypeError:
                    result = fn(item)
                if isinstance(result, list):
                    mapped.extend(result)
                else:
                    mapped.append(result)
            return mapped
        if method == "fill":
            val = args[0] if args else UNDEFINED
            start = int(args[1]) if len(args) > 1 else 0
            end = int(args[2]) if len(args) > 2 else len(arr)
            for i in range(start, end):
                arr[i] = val
            return arr
        if method == "copyWithin":
            return arr
        if method == "at":
            idx = int(args[0]) if args else 0
            if idx < 0:
                idx = len(arr) + idx
            return arr[idx] if 0 <= idx < len(arr) else UNDEFINED
        if method == "keys":
            return list(range(len(arr)))
        if method == "values":
            return arr[:]
        if method == "entries":
            return [[i, v] for i, v in enumerate(arr)]
        if method == "toString":
            return ",".join(js_to_string(item) for item in arr)
        raise Exception(f"Unknown array method: {method}")

    def _flatten(self, arr, depth):
        result = []
        for item in arr:
            if isinstance(item, list) and depth > 0:
                result.extend(self._flatten(item, depth - 1))
            else:
                result.append(item)
        return result

    def exec_member(self, node):
        obj = self._exec(node.object)

        if node.computed:
            prop = self._exec(node.property)
            if isinstance(obj, list):
                if isinstance(prop, str) and prop == "length":
                    return len(obj)
                return obj[int(prop)] if 0 <= int(prop) < len(obj) else UNDEFINED
            if isinstance(obj, str):
                if isinstance(prop, str) and prop == "length":
                    return len(obj)
                idx = int(prop)
                return obj[idx] if 0 <= idx < len(obj) else UNDEFINED
            if isinstance(obj, dict):
                key = js_to_string(prop) if not isinstance(prop, str) else prop
                return obj.get(key, UNDEFINED)
            return UNDEFINED

        prop = node.property

        if obj == "Math":
            if prop == "PI":
                return math.pi
            if prop == "E":
                return math.e
            if prop == "LN2":
                return math.log(2)
            if prop == "LN10":
                return math.log(10)
            if prop == "SQRT2":
                return math.sqrt(2)

        if isinstance(obj, list):
            if prop == "length":
                return len(obj)
            return UNDEFINED

        if isinstance(obj, str):
            if prop == "length":
                return len(obj)
            return UNDEFINED

        if isinstance(obj, dict):
            return obj.get(prop, UNDEFINED)

        if isinstance(obj, JSDate):
            method = getattr(obj, prop, None)
            if method and callable(method):
                return method
            return UNDEFINED

        if obj == "Number":
            if prop == "MAX_SAFE_INTEGER":
                return 2**53 - 1
            if prop == "MIN_SAFE_INTEGER":
                return -(2**53 - 1)
            if prop == "MAX_VALUE":
                return 1.7976931348623157e+308
            if prop == "EPSILON":
                return 2.220446049250313e-16

        return UNDEFINED

    def exec_typeof(self, node):
        if isinstance(node.operand, Identifier):
            try:
                val = self.environment.get(node.operand.name)
            except Exception:
                return "undefined"
        else:
            val = self._exec(node.operand)
        return js_typeof(val)

    def exec_array(self, node):
        result = []
        for el in node.elements:
            if isinstance(el, SpreadElement):
                iterable = self._exec(el.argument)
                if isinstance(iterable, str):
                    result.extend(list(iterable))
                else:
                    result.extend(iterable)
            else:
                result.append(self._exec(el))
        return result

    def exec_object(self, node):
        result = {}
        for prop in node.properties:
            if isinstance(prop, SpreadElement):
                source = self._exec(prop.argument)
                if isinstance(source, dict):
                    result.update(source)
            elif isinstance(prop, ObjectProperty):
                if prop.computed:
                    key = js_to_string(self._exec(prop.key))
                else:
                    key = self._exec(prop.key) if isinstance(prop.key, (StringLiteral, NumberLiteral)) else prop.key
                    if isinstance(key, int):
                        key = str(key)
                value = self._exec(prop.value)
                result[key] = value
        return result