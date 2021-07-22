
common_mistakes = {'איינסטיין': 'אינשטיין', 'אמדי': 'עמדי', 'יייגל': 'ייגל',
                   'עיברי': 'עברי', 'עיזהר': 'יזהר', 'עיצהק': 'יצחק', 'עישי': 'ישי',
                   'ריבה': 'ריבו', 'שלומה': 'שלמה'}

abc = 'אבגדהוזחטיכלמנסעפצקרשת'


def gtol(num) -> str:
    if 1 <= num <= 10:
        return abc[num - 1]
    if 20 <= num <= 100:
        return abc[int(8 + num / 10)]
    if 200 <= num <= 400:
        return abc[int(17 + num / 100)]
    return 'no letter'


lasts = {gtol(20): 'ך', gtol(40): 'ם', gtol(50): 'ן', gtol(80): 'ף', gtol(90): 'ץ'}


def endify(word):
    if word[-1] in lasts.keys():
        return word[:-1] + lasts[word[-1]]
    return word


not_vowels = {'a': {'end': gtol(5), 'start': gtol(1), 'after_vowel': '', 'after_nvowel': ''},
          'e': {'end': gtol(5), 'start': gtol(1), "after_vowel": '', 'after_nvowel': ''},
          'i': {'end': gtol(10), 'start': gtol(70) + gtol(10), "after_vowel": gtol(10), 'after_nvowel': gtol(10) + gtol(10)},
          'o': {'end': gtol(5), 'start': gtol(1) + gtol(6), 'after_vowel': gtol(6), 'after_nvowel': gtol(6)},
          'u': {'end': gtol(6), 'start': gtol(1) + gtol(6), 'after_vowel': gtol(6), 'after_nvowel': gtol(6)},
          'y': {'end': gtol(10), 'start': gtol(10), 'after_vowel': gtol(10), 'after_nvowel': gtol(10)}}


letters = {'b':gtol(2), 'c':gtol(60), 'd':gtol(4),
           'f':gtol(80), 'g':gtol(3), 'h':gtol(5),
           'j':gtol(3), 'k':gtol(100), 'l':gtol(30),
           'm':gtol(40), 'n':gtol(50), 'p':gtol(80),
           'q':gtol(100), 'r':gtol(200), 's':gtol(60),
           't':gtol(9), 'v':gtol(2), 'w':gtol(6) + gtol(6),
           'x':gtol(100) + gtol(60), 'z':gtol(7), '?': gtol(300),
           '!':gtol(20), '|':gtol(90), '.':gtol(400)}

different_start = {'c': gtol(20), 'h':gtol(8)}
different_end = {'t':gtol(400)}


def translate_word(word):
    word = word.lower().replace('oo', 'u').replace('ch', "!")\
        .replace('sh', '?').replace('tz', '|')\
        .replace('th', '.').replace('tt', '.')
    result = ''
    for i in range(len(word)):
        if i != 0 and word[i - 1] == word[i] and word[i] in letters.keys():
            continue
        add = ''
        if word[i] in letters.keys():
            if i == 0 and word[i] in different_start.keys():
                add = different_start[word[i]]
            elif i == len(word) - 1 and word[i] in different_end.keys():
                add = different_end[word[i]]
            else:
                add = letters[word[i]]
        else:
            if i == 0:
                add = not_vowels[word[i]]['start']
            elif i == len(word) - 1:
                add = not_vowels[word[i]]['end']
            elif word[i - 1] in not_vowels.keys():
                add = not_vowels[word[i]]['after_nvowel']
            else:
                add = not_vowels[word[i]]['after_vowel']

        result += add
    result = endify(result)
    if result in common_mistakes.keys():
        return common_mistakes[result]
    return result


def translate_name(name):
    trans = ''
    if ',' in name:
        name = name[:name.find(',')]
    for word in name.split(' '):
        trans += translate_word(word) + " "
    return trans[:-1]
