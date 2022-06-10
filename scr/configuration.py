import json


class Config(object):
    """basic configuration settings loader
    class, which is going to be used later
    on in the code by other modules"""

    def __init__(self, directory: str) -> None:
        self._directory = directory
        self.data = self.load()

    def load(self) -> dict:
        with open(self._directory, 'r') as file:
            data = json.load(file)
        return data

    def __call__(self) -> dict:
        return self.data