class CompileException(Exception):
    def __init__(self, message: str):
        """Compile Exception"""
        self.message = message
