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


rb = ['minsk_5000000000', {}]
admins = {'regions': [], 'districts': [], 'soviets': []}

wb = xlrd.open_workbook('CITY.xls')
sheet = wb.sheet_by_index(0)
for i in range(1, sheet.nrows):
    print(i)
    row = sheet.row_values(i, 0, 6)
    if row == ['', '', '', '', '', '']:
        continue
    if row[2]:
        if row[2] not in rb[1]:
            rb[1][row[2]] = ['', {}]
            for admin in admins['regions']:
                if admin[0:4] in convert_to_translit(row[2]):
                    rb[1][row[2]][0] = admin
                    admins['regions'].remove(admin)
                    break
    else:
        name = convert_to_translit(row[1])+'_'+row[0]
        admins['regions'].append(name)
        admins['districts'].append(name)
        for region in rb[1].items():
            for admin in admins['regions']:
                if admin[0:4] in convert_to_translit(region[0]):
                    rb[1][region[0]][0] = admin
                    admins['regions'].remove(admin)
                    break
        continue
    if row[3]:
        if row[3] not in rb[1][row[2]][1]:
            rb[1][row[2]][1][row[3]] = ['', {}]
            for admin in admins['districts']:
                if admin[0:4] in convert_to_translit(row[3]):
                    rb[1][row[2]][1][row[3]][0] = admin
                    admins['districts'].remove(admin)
                    break
    else:
        admins['districts'].append(convert_to_translit(row[1])+'_'+row[0])
        for region in rb[1].items():
            for district in region[1][1].items():
                for admin in admins['districts']:
                    if admin[0:4] in convert_to_translit(district[0]):
                        rb[1][region[0]][1][district[0]][0] = admin
                        admins['districts'].remove(admin)
                        break
        continue
    if row[4]:
        admins['soviets'].append(convert_to_translit(row[1])+'_'+row[0])
        if row[4] not in rb[1][row[2]][1][row[3]][1]:
            rb[1][row[2]][1][row[3]][1][row[4]] = ['', []]
            for admin in admins['soviets']:
                if admin[0:4] in convert_to_translit(row[4]):
                    rb[1][row[2]][1][row[3]][1][row[4]][0] = admin
                    admins['soviets'].remove(admin)
                    break
        rb[1][row[2]][1][row[3]][1][row[4]][1].append(convert_to_translit(row[1]) + '_' + row[0])
    else:
        admins['soviets'].append(convert_to_translit(row[1]) + '_' + row[0])
        for region in rb[1].items():
            for district in region[1][1].items():
                for soviet in district[1][1].items():
                    for admin in admins['soviets']:
                        if admin[0:4] in convert_to_translit(soviet[0]):
                            rb[1][region[0]][1][district[0]][1][soviet[0]][0] = admin
                            admins['soviets'].remove(admin)
                            break

with open('structure.scs', 'w', encoding='utf-8') as file:
    file.write('republic_of_belarus => nrel_admin_center: ' + rb[0] + ';;\n')
    for region in rb[1].items():
        region_idtf = convert_to_translit(region[0].rsplit(' ', maxsplit=1)[0]) + '_region'
        file.write('republic_of_belarus => nrel_whole_part: ' + region_idtf + ';;\n')
        if region[1][0]:
            file.write(region_idtf + ' => nrel_admin_center: ' + region[1][0] + ';;\n')
        else:
            file.write('\n')
        file.write(region_idtf + ' => nrel_main_idtf: [' + region[0].capitalize() + '](* <- lang_ru;; *);;\n')
        file.write(region_idtf + ' => nrel_main_idtf: [' + convert_to_translit(region[0].rsplit(' ', maxsplit=1)[0], False) + ' region](* <- lang_eng;; *);;\n')
        file.write(region_idtf + ' <- sc_node_not_relation;;\n')
        for district in region[1][1].items():
            district_idtf = convert_to_translit(district[0]) + '_district'
            file.write('    ' + region_idtf + ' => nrel_whole_part: ' + district_idtf + ';;\n')
            if district[1][0]:
                file.write('    ' + district_idtf + ' => nrel_admin_center: ' + district[1][0] + ';;\n')
            else:
                file.write('')
            file.write('    ' + district_idtf + ' => nrel_main_idtf: [' + district[0] + ' район](* <- lang_ru;; *);;\n')
            file.write('    ' + district_idtf + ' => nrel_main_idtf: [' + convert_to_translit(district[0], False) + ' district](* <- lang_eng;; *);;\n')
            file.write('    ' + region_idtf + ' <- sc_node_not_relation;;\n')
            for soviet in district[1][1].items():
                if 'Совет' in soviet[0]:
                    soviet_idtf = convert_to_translit(soviet[0].rsplit(' ', maxsplit=1)[0]) + '_soviet'
                    file.write('        ' + soviet_idtf + ' => nrel_main_idtf: [' + soviet[0].capitalize() + '](* <- lang_ru;; *);;\n')
                    file.write('        ' + soviet_idtf + ' => nrel_main_idtf: [' + convert_to_translit(soviet[0].rsplit(' ', maxsplit=1)[0], False) + ' soviet](* <- lang_eng;; *);;\n')
                else:
                    soviet_idtf = convert_to_translit(soviet[0]) + '_soviet'
                    file.write('        ' + soviet_idtf + ' => nrel_main_idtf: [' + soviet[0] + ' совет](* <- lang_ru;; *);;\n')
                    file.write('        ' + soviet_idtf + ' => nrel_main_idtf: [' + convert_to_translit(soviet[0], False) + ' soviet](* <- lang_eng;; *);;\n')
                if soviet[1][0]:
                    file.write('        ' + soviet_idtf + ' => nrel_admin_center: ' + soviet[1][0] + ';;\n')
                else:
                    file.write('')
                file.write('        ' + district_idtf + ' => nrel_whole_part: ' + soviet_idtf + ';;\n')
                file.write('        ' + soviet_idtf + ' <- sc_node_not_relation;;\n')
                for village in soviet[1][1]:
                    file.write('            ' + soviet_idtf + ' => nrel_whole_part: ' + village + ';;\n')
