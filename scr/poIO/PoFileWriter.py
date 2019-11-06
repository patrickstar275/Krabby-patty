from . import PoDataStructs


class PoFileWriter:
    def __init__(self):
        self._file_data = None

    def set_data(self, file_data):
        if isinstance(file_data, PoDataStructs.PoFileStruct):
            self._file_data = file_data
        else:
            raise TypeError("set_data: file_data must be instance of PoFileStruct. ")

    def write(self, file_path):
        with open(file_path, 'w', encoding="utf-8") as outf:
            for b in self._file_data.get_blocks():
                for e in b.extra:
                    outf.write(e + '\n')
                for u in b.get_units():
                    outf.write('msgid "')
                    for id in u.segments:
                        outf.write(id)
                    outf.write('"\n')
                    outf.write('msgstr ')
                    for str in u.result:
                        outf.write('"' + str + '"\n')
                outf.write('\n')
