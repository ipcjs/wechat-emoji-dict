from pypinyin import lazy_pinyin, Style
from zipfile import ZipFile
import flypy
import re

_RE_ENGLISH = re.compile(r'\w+', re.ASCII)


def kanji_to_pinyin(kanji: str):
    if _RE_ENGLISH.fullmatch(kanji):
        # 纯英文字母, 转小写就行
        return ([kanji.lower()], True)
    return (lazy_pinyin(kanji, style=Style.NORMAL), False)

def save_to_gboard(_list, py_type='pinyin', lang='zh-CN'):
    base_path = f'out/wechat-emoji-gboard-{py_type}'
    dict_file = base_path+'.txt'
    zip_file = base_path + '.zip'

    with open(dict_file, 'w', encoding='utf-8') as f:
        f.write('# Gboard Dictionary version:1\n')
        for item in _list:
            py = item['pinyin']
            if py_type == 'flypy' and not item['is_english']:
                py = list(map(lambda s: flypy.todouble(s), py))
            f.write('\t'.join((''.join(py), item['word'], lang)) + '\n')
    # archive
    with ZipFile(zip_file, 'w') as f:
        f.write(dict_file, 'dictionary.txt')

def save_to_rime(list):
    with open('out/wechat-emoji.dict.yaml', 'w', encoding='utf-8') as f:
        f.write('''# wechat-emoji
---
name: wechat-emoji
version: "0.1"
sort: by_weight
...
''')
        for item in list:
            if item['is_english']:
                print(f'skip: {item}')
            else:
                f.write(item['word'] + '\t' + ' '.join(item['pinyin']) + '\n')

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
                pinyin, is_english = kanji_to_pinyin(kanji)
                list.append({
                    'word': word,
                    'pinyin': pinyin,
                    'is_english': is_english,
                })
    save_to_rime(list)
    save_to_gboard(list)
    save_to_gboard(list, py_type='flypy')


if __name__ == '__main__':
    main()
    print('completed.')
