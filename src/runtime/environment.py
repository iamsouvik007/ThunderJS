class Environment:
    def __init__(self):
        self.variables = {}

    def define(self, name, value):
        self.variables[name] = value

    def get(self, name):
        if name not in self.variables:
            raise Exception(
                f"Variable '{name}' not defined"
            )

        return self.variables[name]