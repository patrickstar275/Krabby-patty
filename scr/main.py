from poIO.PoFileReader import PoFileReader
from poIO.PoFileFilter import PoFileFilter
from poIO.PoUnitConnector import PoUnitConnector
from poIO.PoFileWriter import PoFileWriter
from Translators import BaiduTranslator

# infilePath = "../po/ultimate-member-zh_CN.po"
infilePath = "../po/wedevs-project-manager-zh_CN.po"
outfilePath = "../out/out.po"

if __name__ == "__main__":
    reader = PoFileReader()
    filte = PoFileFilter()
    reader.read(infilePath)
    filte.process(reader.get_data())

    result = filte.get_file_struct()
    connect = PoUnitConnector()
    for b_idx in range(len(result.get_blocks())):
        b = result.get_blocks()[b_idx]
        for u in b.get_units():
            if len(u.result) == 1 and u.result[0] == '':
                connect.set_unit(u)
                translate_list = connect.get_translate_list()
                translated_list = []
                for line in translate_list:
                    res = BaiduTranslator.translate_auto(line)
                    translated_list.append(('' if res is None else res))
                res_list = connect.set_translate_list(translated_list)
                res_str = ""
                for res_seg in res_list:
                    res_str += res_seg
                u.result[0] = res_str
        print("Translated {:.2f}%".format((b_idx / len(result.get_blocks())) * 100))

    writer = PoFileWriter()
    writer.set_data(result)
    writer.write(outfilePath)
