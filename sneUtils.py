class Pointer():

    def __init__(self, obj) -> None:
        self.obj = obj

    def set(self, obj):
        self.obj = obj

    def get(self):
        return self.obj