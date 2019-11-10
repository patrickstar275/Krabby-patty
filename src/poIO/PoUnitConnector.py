from . import PoDataStructs


class PoUnitConnector:
    def __init__(self):
        self._elem = []
        self._map = []

    def set_unit(self, unit):
        if isinstance(unit, PoDataStructs.PoTranslateUnit):
            self._elem = unit.segments
            self._map = unit.segments_map
        else:
            raise TypeError("set_unit: unit must be instance of PoTranslateUnit")

    def get_translate_list(self):
        list = []
        str = ""
        for idx in range(len(self._elem)):
            if self._map[idx] == 0:
                if len(str) > 0:
                    list.append(str)
                str = ""
            else:
                if len(str) > 0:
                    str += " "
                str += self._elem[idx]
        if len(str) > 0:
            list.append(str)
        return list

    def set_translate_list(self, list):
        new_list = []
        if len(list) != len(self.get_translate_list()):
            raise RuntimeError("List length not match!")
        idx = 0
        pointer = 0
        while idx < len(self._elem):
            if self._map[idx] == 0:
                new_list.append(self._elem[idx])
                idx += 1
            else:
                new_list.append(list[pointer])
                while idx < len(self._elem) and self._map[idx] == 1:
                    idx += 1
                pointer += 1
        return new_list
