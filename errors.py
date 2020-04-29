class CompilerError(BaseException):
    def __init__(self, *args):
        super().__init__(' '.join(args))
        self.args = args

    def again(self, *args):
        return self.__class__(' '.join(self.args + args))