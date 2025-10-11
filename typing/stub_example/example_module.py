def concatenate_obj(s1: str, s2: str):
    """Concatenates two strings."""
    return s1 + s2

class DataProcessor:
    version = "1.0.0"
    def __init__(self, data_list):
        self.data = data_list

    def get_first_item(self):
        if self.data:
            return self.data
        return None

    def add_item(self, item):
        self.data.append(item)