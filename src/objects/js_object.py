class JSObject:
    @staticmethod
    def execute_static(method, args):
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
