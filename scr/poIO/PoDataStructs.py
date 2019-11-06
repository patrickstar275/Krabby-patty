class PoBlock:
    def __init__(self):
        self.msgid = []
        self.msgstr = []
        self.extra = []

    def print(self):
        print("Msgid:", self.msgid)
        print("Msgstr:", self.msgstr)
        print("Extra:", self.extra)


class PoFile:
    def __init__(self):
        self._blocks = []

    def add_block(self, block):
        if isinstance(block, PoBlock):
            self._blocks.append(block)
        else:
            raise TypeError("add_block: block must be instance of PoBlock.")

    def get_blocks(self):
        return self._blocks


class PoTranslateUnit:
    def __init__(self):
        self.segments = []
        self.segments_map = []
        self.result = []


class PoTranslateBlock:
    def __init__(self):
        self.extra = []
        self._units = []

    def append_unit(self, unit):
        if isinstance(unit, PoTranslateUnit):
            self._units.append(unit)
        else:
            raise TypeError("append_unit: unit must be instance of PoTranslateUnit.")

    def get_units(self):
        return self._units

class PoFileStruct:
    def __init__(self):
        self._blocks = []

    def add_block(self, block):
        if isinstance(block, PoTranslateBlock):
            self._blocks.append(block)
        else:
            raise TypeError("add_block: block must be instance of PoTranslateBlock")

    def get_blocks(self):
        return self._blocks
