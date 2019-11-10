class PoBlockFilter():
    def __init__(self):
        self._segments = []
        self._segments_map = []

    def process(self, raw_msg):
        self._segments, self._segments_map = self._filte_html(raw_msg)
        self._segments, self._segments_map = self._filte_brackets_0(self._segments, self._segments_map)
        self._segments, self._segments_map = self._filte_escapes_0(self._segments, self._segments_map)
        self._segments, self._segments_map = self._filte_html_entities(self._segments, self._segments_map)
        self._segments, self._segments_map = self._filte_escapes_1(self._segments, self._segments_map)
        self._segments, self._segments_map = self._filte_escapes_2(self._segments, self._segments_map)
        self._segments, self._segments_map = self._optimizer(self._segments, self._segments_map)

    def get_segments(self):
        return self._segments

    def get_segments_map(self):
        return self._segments_map

    def _filte_html(self, raw_str):
        sum = 0
        addl = 0
        addr = 0
        for c in raw_str:
            if c == "<":
                sum += 1
            elif c == ">":
                sum -= 1
            if sum < 0:
                addl += -sum
                sum = 0
        addr = sum
        fited_str = "<" * addl + raw_str + ">" * addr
        sum = 0
        segs = []
        segs_map = []
        seg = ""
        seg_flag = 1
        for idx in range(len(fited_str)):
            c = fited_str[idx]
            if idx == 0 and c == "<":
                seg_flag = 0
            if c == "<":
                if len(seg) > 0:
                    segs.append(seg)
                    segs_map.append(seg_flag)
                    seg_flag = 0
                    seg = ""
                sum += 1
                seg += c
                if idx == len(fited_str) - 1:
                    if len(seg) > 0:
                        segs.append(seg)
                        segs_map.append(seg_flag)
            elif c == ">":
                sum -= 1
                seg += c
                if idx == len(fited_str) - 1:
                    if len(seg) > 0:
                        segs.append(seg)
                        segs_map.append(seg_flag)
            elif sum == 0 and idx != 0 and c != ">":
                if len(seg) > 0 and seg_flag == 0:
                    segs.append(seg)
                    segs_map.append(seg_flag)
                    seg_flag = 1
                    seg = ""
                seg += c
                if idx == len(fited_str) - 1:
                    if len(seg) > 0:
                        segs.append(seg)
                        segs_map.append(seg_flag)
            elif idx == len(fited_str) - 1:
                if len(seg) > 0:
                    segs.append(seg)
                    segs_map.append(seg_flag)
            else:
                seg += c
        if addl > 0:
            segs[0] = segs[0][addl:]
        if addr > 0:
            segs[-1] = segs[-1][:-addr]
        return segs, segs_map

    def _filte_html_entities(self, segs, segs_map):
        seg = ""
        new_segs = []
        new_segs_map = []
        for idx in range(len(segs)):
            if segs_map[idx] == 1:
                str = segs[idx]
                str_idx = 0
                while str_idx < len(str):
                    if str[str_idx:str_idx + 2] == '&#':
                        if len(seg) > 0:
                            new_segs.append(seg)
                            new_segs_map.append(1)
                            seg = ""
                        fpos = str_idx + 2
                        for fidx in range(str_idx, len(str)):
                            if str[fidx] == ";":
                                fpos = fidx + 1
                                break
                        new_segs.append(chr(int(str[str_idx:fpos].replace("&#", '').replace(';', ''))))
                        new_segs_map.append(1)
                        str_idx += fpos - str_idx
                    else:
                        seg += str[str_idx]
                        if str_idx == len(str) - 1:
                            new_segs.append(seg)
                            new_segs_map.append(1)
                            seg = ""
                        str_idx += 1
            else:
                new_segs.append(segs[idx])
                new_segs_map.append(segs_map[idx])
        return new_segs, new_segs_map

    def _filte_brackets_0(self, segs, segs_map):
        new_segs = []
        new_segs_map = []
        new_segs_out = []
        new_segs_map_out = []
        for idx in range(len(segs)):
            if segs_map[idx] == 1:
                raw_str = segs[idx]
                sum = 0
                addl = 0
                addr = 0
                for c in raw_str:
                    if c == "[":
                        sum += 1
                    elif c == "]":
                        sum -= 1
                    if sum < 0:
                        addl += -sum
                        sum = 0
                addr = sum
                fited_str = "[" * addl + raw_str + "]" * addr
                sum = 0
                seg = ""
                seg_flag = 1
                for idx in range(len(fited_str)):
                    c = fited_str[idx]
                    if idx == 0 and c == "[":
                        seg_flag = 0
                    if c == "[":
                        if len(seg) > 0:
                            new_segs.append(seg)
                            new_segs_map.append(seg_flag)
                            seg_flag = 0
                            seg = ""
                        sum += 1
                        seg += c
                        if idx == len(fited_str) - 1:
                            if len(seg) > 0:
                                new_segs.append(seg)
                                new_segs_map.append(seg_flag)
                    elif c == "]":
                        sum -= 1
                        seg += c
                        if idx == len(fited_str) - 1:
                            if len(seg) > 0:
                                new_segs.append(seg)
                                new_segs_map.append(seg_flag)
                    elif sum == 0 and idx != 0 and c != "]":
                        if len(seg) > 0 and seg_flag == 0:
                            new_segs.append(seg)
                            new_segs_map.append(seg_flag)
                            seg_flag = 1
                            seg = ""
                        seg += c
                        if idx == len(fited_str) - 1:
                            if len(seg) > 0:
                                new_segs.append(seg)
                                new_segs_map.append(seg_flag)
                    elif idx == len(fited_str) - 1:
                        if len(seg) > 0:
                            new_segs.append(seg)
                            new_segs_map.append(seg_flag)
                    else:
                        seg += c
                if addl > 0:
                    new_segs[0] = new_segs[0][addl:]
                if addr > 0:
                    new_segs[-1] = new_segs[-1][:-addr]
                new_segs_out += new_segs
                new_segs_map_out += new_segs_map
            else:
                new_segs_out.append(segs[idx])
                new_segs_map_out.append(segs_map[idx])
        return new_segs_out, new_segs_map_out

    def _filte_escapes_0(self, segs, segs_map):
        seg = ""
        new_segs = []
        new_segs_map = []
        for idx in range(len(segs)):
            if segs_map[idx] == 1:
                str = segs[idx]
                str_idx = 0
                while str_idx < len(str):
                    if str[str_idx] == '"':
                        if len(seg) > 0:
                            new_segs.append(seg)
                            new_segs_map.append(1)
                            seg = ""
                        fpos = str_idx
                        for fidx in range(str_idx + 1, len(str)):
                            if str[fidx] == '"':
                                fpos = fidx + 1
                                break
                        new_segs.append(str[str_idx:fpos])
                        new_segs_map.append(0)
                        str_idx += fpos - str_idx
                    else:
                        seg += str[str_idx]
                        if str_idx == len(str) - 1:
                            new_segs.append(seg)
                            new_segs_map.append(1)
                            seg = ""
                        str_idx += 1
            else:
                new_segs.append(segs[idx])
                new_segs_map.append(segs_map[idx])
        return new_segs, new_segs_map

    def _filte_escapes_1(self, segs, segs_map):
        seg = ""
        new_segs = []
        new_segs_map = []
        for idx in range(len(segs)):
            if segs_map[idx] == 1:
                str = segs[idx]
                str_idx = 0
                while str_idx < len(str):
                    if str[str_idx] == '%':
                        if len(seg) > 0:
                            new_segs.append(seg)
                            new_segs_map.append(1)
                            seg = ""
                        fpos = str_idx + 2
                        for fidx in range(str_idx, len(str)):
                            if str[fidx] == " ":
                                fpos = fidx + 1
                                break
                        new_segs.append(str[str_idx:fpos])
                        new_segs_map.append(0)
                        str_idx += fpos - str_idx
                    else:
                        seg += str[str_idx]
                        if str_idx == len(str) - 1:
                            new_segs.append(seg)
                            new_segs_map.append(1)
                            seg = ""
                        str_idx += 1
            else:
                new_segs.append(segs[idx])
                new_segs_map.append(segs_map[idx])
        return new_segs, new_segs_map

    def _filte_escapes_2(self, segs, segs_map):
        seg = ""
        new_segs = []
        new_segs_map = []
        for idx in range(len(segs)):
            if segs_map[idx] == 1:
                str = segs[idx]
                str_idx = 0
                while str_idx < len(str):
                    if str[str_idx] == '$':
                        if len(seg) > 0:
                            new_segs.append(seg)
                            new_segs_map.append(1)
                            seg = ""
                        fpos = str_idx + 2
                        for fidx in range(str_idx, len(str)):
                            if str[fidx] == " ":
                                fpos = fidx + 1
                                break
                        new_segs.append(str[str_idx:fpos])
                        new_segs_map.append(0)
                        str_idx += fpos - str_idx
                    else:
                        seg += str[str_idx]
                        if str_idx == len(str) - 1:
                            new_segs.append(seg)
                            new_segs_map.append(1)
                            seg = ""
                        str_idx += 1
            else:
                new_segs.append(segs[idx])
                new_segs_map.append(segs_map[idx])
        return new_segs, new_segs_map

    def _optimizer(self, segs, segs_map):
        new_segs_map = []
        for idx in range(len(segs)):
            seg = segs[idx].strip()
            if\
                seg == '.' or\
                seg == '\\' or\
                seg == '':
                new_segs_map.append(0)
            else:
                new_segs_map.append(segs_map[idx])
        return segs, new_segs_map
