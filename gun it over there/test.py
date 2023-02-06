class Test():
    def __init__(self):
        self.offset = [0,0]

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self,offset):
        print("set")
        self._offset = offset

test = Test()
test.offset[1] -= 1