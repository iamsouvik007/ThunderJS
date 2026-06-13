class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def define(self, name, value):
        self.variables[name] = value

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise Exception(f"Variable '{name}' not defined")

    def set(self, name, value):
        if name in self.variables:
            self.variables[name] = value
            return
        if self.parent:
            self.parent.set(name, value)
            return
        raise Exception(f"Variable '{name}' not defined")