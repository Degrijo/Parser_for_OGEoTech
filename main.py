import overpy
import requests
import xlrd

alphabet = {'А': 'A', 'а': 'a', 'Б': 'B', 'б': 'b', 'В': 'V', 'в': 'v', 'Г': 'G', 'г': 'g', 'Д': 'D', 'д': 'd',
            'Е': 'E',
            'е': 'e', 'Ё': 'Yo', 'ё': 'yo', 'Ж': 'Zh', 'ж': 'zh', 'З': 'Z', 'з': 'z', 'И': 'I', 'и': 'i', 'Й': 'J',
            'й': 'j',
            'К': 'K', 'к': 'k', 'Л': 'L', 'л': 'l', 'М': 'M', 'м': 'm', 'Н': 'N', 'н': 'n', 'О': 'O', 'о': 'o',
            'П': 'P', 'п': 'p',
            'Р': 'R', 'р': 'r', 'С': 'S', 'с': 's', 'Т': 'T', 'т': 't', 'У': 'U', 'у': 'u', 'Ф': 'F', 'ф': 'f',
            'Х': 'Kh', 'х': 'kh',
            'Ц': 'Ts', 'ц': 'ts', 'Ч': 'Ch', 'ч': 'ch', 'Ш': 'Sh', 'ш': 'sh', 'Щ': 'Shch', 'щ': 'shch', 'Ъ': '',
            'ъ': '', 'Ы': 'Y', 'ы': 'y', 'Ь': '', 'ь': '', 'Э': 'E', 'э': 'e', 'Ю': 'Yu', 'ю': 'yu', 'Я': 'Ya',
            'я': 'ya', ' ': '_', '-': '_', '(': '_', ')': '', '/': '', 'i': '1', '.': '_'}


def convert_to_translit(word, severity=True):
    if severity:
        word = word.lower()
    else:
        word = word.capitalize()
    new = ""
    for ch in word:
        if ch.isdigit() or ch in [' ', '(', ')', '/'] and not severity:
            new += ch
        else:
            new += alphabet[ch]
    return new


def translate(text):
    key = 'trnsl.1.1.20181208T105434Z.0f39ab1008611643.4cf37073d9f2b4a1b126c71a5caa228b4ece1309'
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
    r = requests.post(url, data={'key': key, 'text': text, 'lang': 'ru-en'})
    return eval(r.text)['text'][0]


def get_inf(row, i):  # ['1204755001', 'Арабовщина', 'БРЕСТСКАЯ ОБЛАСТЬ', 'Барановичский', 'Городищенский поселковый Совет', 'аг.']
    inf = {'idtf': convert_to_translit(row[1])+'_'+row[0], 'name_ru': row[1] + ' ' + row[0],
           'name_en': convert_to_translit(row[1], False) + ' ' + row[0]}

    if row[4]:
        if 'Совет' in row[4]:
            inf['parent_idtf'] = convert_to_translit(row[4].rsplit(' ', maxsplit=1)[0]) + '_soviet'
            #parent_name_eng = convert_to_translit(row[4].rsplit(' ', maxsplit=1)[0], False) + ' soviet'
            #parent_name_ru = row[4].capitalize()
        else:
            inf['parent_idtf'] = convert_to_translit(row[4]) + '_soviet'
            '''parent_name_eng = convert_to_translit(row[4], False) + ' soviet'
            parent_name_ru = row[4] + ' совет'
        with open('soviets.scs', 'r+', encoding='utf-8') as soviets:
            here = False
            strings = soviets.readlines()
            for i in range(0, len(strings), 3):
                if inf['parent_idtf'] in strings[i]:
                    here = True
                    break
            if not here:
                new = '{0} <- {1};;'.format(inf['parent_idtf'], convert_to_translit(row[3]) + '_district') + '\n{0} => nrel_main_idtf: [{1}](* <- lang_ru;; *);;{0} => nrel_main_idtf: [{2}](* <- lang_en;; *);;'.format(inf['parent_idtf'], parent_name_ru, parent_name_eng) + '\n'
                new += '{} <- sc_node_not_relation;;'.format(inf['parent_idtf']) + '\n'
                soviets.write(new)'''
    elif row[3]:
        inf['parent_idtf'] = convert_to_translit(row[3]) + '_district'
        '''parent_name_eng = convert_to_translit(row[3], False) + ' district'
        with open('districts.scs', 'r+', encoding='utf-8') as districts:
            here = False
            strings = districts.readlines()
            for i in range(0, len(strings), 4):
                if inf['parent_idtf'] in strings[i]:
                    here = True
                    break
            if not here:
                new = '{0} <- {1};;'.format(inf['parent_idtf'], convert_to_translit(row[2].rsplit(' ', maxsplit=1)[0]) + '_region') + '\n{0} => nrel_main_idtf: [{1}](* <- lang_ru;; *);;{0} => nrel_main_idtf: [{2}](* <- lang_en;; *);;'.format(inf['parent_idtf'], row[3] + ' район', parent_name_eng) + '\n'
                if i == 1:
                    new += convert_to_translit('Барановичи')+'_1410000000\n'
                elif i == 358:
                    new += convert_to_translit('Брест') + '_1401000000\n'
                elif i == 1669:
                    new += convert_to_translit('Пинск') + '_1445000000\n'
                else:
                    prev = sheet.row_values(i - 1, 0)
                    new += convert_to_translit(prev[1]) + '_' + prev[0] + '\n'
                new += '{} <- sc_node_not_relation;;'.format(inf['parent_idtf']) + '\n'
                districts.write(new)'''
    elif row[2]:
        inf['parent_idtf'] = convert_to_translit(row[2].rsplit(' ', maxsplit=1)[0]) + '_region'
        '''parent_name_eng = convert_to_translit(row[2].rsplit(' ', maxsplit=1)[0], False) + ' region'
        with open('regions.scs', 'r+', encoding='utf-8') as regions:
            here = False
            strings = regions.readlines()
            for i in range(0, len(strings), 4):
                if inf['parent_idtf'] in strings[i]:
                    here = True
                    break
            if not here:
                new = '{0} <- {1};;'.format(inf['parent_idtf'], 'republic_of_belarus') + '\n' + '{0} => nrel_main_idtf: [{1}](* <- lang_ru;; *);;{0} => nrel_main_idtf: [{2}](* <- lang_en;; *);;'.format(inf['parent_idtf'], row[2].capitalize(), parent_name_eng) + '\n'
                prev = sheet.row_values(i - 1, 0)
                new += '{0} => nrel_admin_center: {1};;'.format(inf['parent_idtf'], convert_to_translit(prev[1]) + '_' + prev[0]) + '\n' + '{} <- sc_node_not_relation;;'.format(inf['parent_idtf']) + '\n'
                regions.write(new)'''
    else:
        inf['parent_idtf'] = 'republic_of_belarus'
    if row[5] == 'аг.' or row[5] == 'с.':
        inf['type'] = 'agro_town'
    elif row[5] == 'д.' or row[5] == 'д':
        inf['type'] = 'village'
    elif row[5] == 'гп':
        inf['type'] = 'urban_village'
    elif row[5] == 'г.' or row[5] == 'г':
        inf['type'] = 'town'
    elif row[5] == 'снп':
        inf['type'] = 'rural_locality'
    elif row[5] == 'х.' or row[5] == 'х':
        inf['type'] = 'farm'
    elif row[5] == 'п.' or row[5] == 'п':
        inf['type'] = 'township'
    elif row[5] == 'рп':
        inf['type'] = 'working_village'
    elif row[5] == 'кп':
        inf['type'] = 'resort_settlement'
    elif row[5] == 'пгт':
        inf['type'] = 'settlement'
    query = api.query("""node["name"="{}"]["addr:country"="BY"];out body;""".format(row[1]))
    if query.nodes:
        if 'wikidata' in query.nodes[0].tags:
            inf['wiki_data'] = query.nodes[0].tags['wikidata']
        else:
            inf['wiki_data'] = ''
        if 'population' in query.nodes[0].tags:
            inf['population'] = query.nodes[0].tags['population']
        else:
            inf['population'] = ''
    else:
        inf['wiki_data'] = ''
        inf['population'] = ''
    return inf


def create_scs(inf, template):
    print(inf['name_ru'])
    for i in range(len(template)):
        template[i] = template[i].replace('~1', inf['idtf'])
    template[0] = template[0].replace('~2', inf['type'])
    template[2] = template[2].replace('~2', inf['name_ru'])
    template[3] = template[3].replace('~2', inf['name_en'])
    template[4] = template[4].replace('~2', inf['parent_idtf'])
    if inf['population']:
        template[5] = template[5].replace('~2', inf['population'])
    else:
        template[5] = ''
    if inf['wiki_data']:
        template[6] = template[6].replace('~2', inf['wiki_data'])
    else:
        template[6] = ''
    if inf['type'] == 'town':
        template[7] = template[7].replace('~2', inf['name_ru'].split(' ')[0])
    else:
        template[7] = ""
    return template


api = overpy.Overpass()
wb = xlrd.open_workbook('CITY.xls')
sheet = wb.sheet_by_index(0)
#for i in range(27231, sheet.nrows):
inf = get_inf(sheet.row_values(23674, 0, 6), 23674)
with open('output/' + inf['idtf']+'.scs', 'w', encoding='utf-8') as defenition:
    template = open('template.scs', 'r', encoding='utf-8')
    defenition.write('\n'.join(create_scs(inf, template.readlines())))
