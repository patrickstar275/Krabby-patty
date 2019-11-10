#from PoDataStructs import *
from . import PoDataStructs
import re


class PoFileReader:
    def __init__(self):
        self._fileData = PoDataStructs.PoFile()

    def read(self, filename):
        try:
            with open(filename, 'r', encoding="utf-8") as in_f:
                file_lines = in_f.readlines()
                file_blocks = []
                start = 0
                for idx in range(len(file_lines)):
                    line = file_lines[idx]
                    if len(self._strip_rn(line)) == 0:
                        file_blocks.append(file_lines[start:idx])
                        start = idx + 1
                    elif idx == len(file_lines) - 1:
                        file_blocks.append(file_lines[start:])
                for block in file_blocks:
                    data = self._read_block(block)
                    self._fileData.add_block(data)
        except Exception as e:
            print(e)

    @staticmethod
    def _strip_rn(line_str):
        return line_str.replace('\n', '').replace('\r', '').strip()

    @staticmethod
    def _strip_line(line_str):
        pattern = re.compile('(?<=\")(.+)(?=\")')
        result = pattern.search(line_str)
        if result is None:
            return ""
        else:
            return result.group().strip()

    def _read_block(self, lines):
        try:
            idx = 0
            block_entries = []
            block = PoDataStructs.PoBlock()
            while idx < len(lines):
                line = lines[idx]
                if line[0] == '#':
                    block.extra.append(self._strip_rn(line))
                    idx += 1
                    continue
                if line.find("msgid") == 0:
                    msgid = []
                    msgstr = []
                    while line.find("msgstr") != 0:
                        idx += 1
                        if len(self._strip_rn(line)) > 0:
                            msgid.append(self._strip_line(line))
                        line = lines[idx]
                    line = lines[idx]
                    if len(self._strip_rn(line)) > 0:
                        msgstr.append(self._strip_line(line))
                    while idx < len(lines) - 1 and len(self._strip_rn(line)) > 0:
                        idx += 1
                        line = lines[idx]
                        if len(self._strip_rn(line)) > 0:
                            msgstr.append(self._strip_line(line))
                    block_entries.append((msgid, msgstr))
                idx += 1
            if len(block_entries) > 1:
                raise RuntimeError("Block have more than one entry.")
            block.msgid = block_entries[0][0]
            block.msgstr = block_entries[0][1]
            return block
        except Exception as e:
            print(e)

    def get_data(self):
        return self._fileData
