class GenesisMemory:
    def __init__(self):
        self.short_term = {}
        self.long_term = {}

    def save_context(self, key: str, value: str, long: bool = False):
        if long:
            self.long_term[key] = value
        else:
            self.short_term[key] = value

    def recall(self, key: str) -> str:
        return self.short_term.get(key) or self.long_term.get(key, "∅")

    def forget(self, key: str):
        self.short_term.pop(key, None)
        self.long_term.pop(key, None)
