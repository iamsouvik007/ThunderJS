class JSArray:
    def __init__(self, arr, strict_equal):
        self.arr = arr
        self.strict_equal = strict_equal

    def execute(self, method, args):
        from src.utils.js_helpers import UNDEFINED, js_to_string, js_to_boolean
        arr = self.arr
        
        def _flatten(a, d):
            res = []
            for item in a:
                if isinstance(item, list) and d > 0:
                    res.extend(_flatten(item, d - 1))
                else:
                    res.append(item)
            return res

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
                if self.strict_equal(arr[i], search):
                    return i
            return -1
        if method == "lastIndexOf":
            search = args[0] if args else UNDEFINED
            for i in range(len(arr) - 1, -1, -1):
                if self.strict_equal(arr[i], search):
                    return i
            return -1
        if method == "includes":
            search = args[0] if args else UNDEFINED
            return any(self.strict_equal(item, search) for item in arr)
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
            return _flatten(arr, depth)
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
