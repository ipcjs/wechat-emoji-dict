from pypinyin import pinyin, lazy_pinyin, Style
from zipfile import ZipFile
import flypy
import re

_RE_ENGLISH = re.compile(r'\w+', re.ASCII)


def kanji_to_pinyin(kanji: str, py_type='pinyin') -> str:
    if _RE_ENGLISH.fullmatch(kanji):
        # 纯英文字母, 转小写就行
        return kanji.lower()
    py = lazy_pinyin(kanji, style=Style.NORMAL)
    if py_type == 'flypy':
        py = list(map(lambda s: flypy.todouble(s), py))
    return ''.join(py)


def save_to_gboard(list, py_type='pinyin', lang='zh-CN'):
    base_path = f'out/wechat-emoji-gboard-{py_type}'
    dict_file = base_path+'.txt'
    zip_file = base_path + '.zip'

    with open(dict_file, 'w', encoding='utf-8') as f:
        f.write('# Gboard Dictionary version:1\n')
        for item in list:
            f.write('\t'.join((item[py_type], item['word'], lang)) + '\n')
    # archive
    with ZipFile(zip_file, 'w') as f:
        f.write(dict_file, 'dictionary.txt')


def main():
    list = []
    with open('source.txt', 'r', encoding='utf-8') as f:
        for line in f:
            segments = line.rstrip('\n').split('\t')
            word = segments[0]
            kanji_list = [word.strip('[]')]
            if len(segments) > 1:
                kanji_list.extend(segments[1].split(','))
            for kanji in kanji_list:
                list.append({
                    'word': word,
                    'pinyin': kanji_to_pinyin(kanji),
                    'flypy': kanji_to_pinyin(kanji, py_type='flypy'),
                })
    save_to_gboard(list)
    save_to_gboard(list, py_type='flypy')


if __name__ == '__main__':
    main()
    print('completed.')
