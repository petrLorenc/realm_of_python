class MyCode:

    def __init__(self):
        self.values = {}

    def set_value(self, key, value):
        self.values[key] = self.values.get(key, 0) + value

    def get_value(self, key):
        return self.values[key]

    def clear(self):
        pass