class Vocab:
    def __init__(self, chars, pinyin, defin):
        self.chars = chars
        self.pinyin = pinyin
        self.defin = defin

    def __str__(self):
        return f"{self.chars}\t{self.pinyin}\t{self.defin}"
    def getChars(self):
        return self.chars
    def getPinyin(self):
        return self.pinyin
    def getDefin(self):
        return self.defin
    