class Model():
    __count = 0

    def __init__(self, name, path2model, path2defaults):
        #super().__init__()
        self.name = name
        self.id = Block.__count
        self.path2model = path2model
        self.path2defaults = path2defaults
        Block.__count += 1
        pass
    
    def execute(self):
        print(self.name)
        print(self.id)
        pass