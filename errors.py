class UnparseableText(Exception):
    def __init__(self, text):
        self.error_text = text