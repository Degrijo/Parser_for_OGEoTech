from os import listdir


for node in listdir('output/'):
    with open('output/' + node, 'r+', encoding='utf-8') as file:
        text = file.readlines()
        if len(text) > 10:
            text.pop(8)
            for _ in range(text.count('\n')):
                text.remove('\n')
            file.seek(0)
            file.write(''.join(text))
            file.truncate()
