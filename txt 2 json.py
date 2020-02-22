import json

index = []
file = open('index.txt', mode = 'r', encoding = 'UTF-8')
for lines in file.readlines():
    temp = lines.split('\\ ')
    path = './character\\' + temp[-1][0] + '\\' + temp[0].split('.')[0] + '.txt'
    index.append(path)
file.close()

for filepath in index:
    if filepath != './character\\\n\\\n.txt':
        file = open(filepath, mode = 'r', encoding = 'UTF-8')
        dict1 = {'日文名':'', '中文名':'', '作戰':'', '卡池':'', 'ep1':'', 'ep3':'無', '特效':'無', 'EX特性':'無', '插畫':'', '聲優':''}
        i, content, ep1, ep3, ep, j = 0, '', [], [], False, False
        for lines in file.readlines():
            if i == 0:
                lines.replace('  ', ' ')
                temp = lines.split(' ')
                dict1['日文名'] = temp[-1].strip()
                dict1['中文名'] = temp[0].strip()
            elif i == 1 or i == 2:
                command, description = lines.strip().split("：")
                dict1[command] = description.strip()
            elif lines.startswith('ep3') and ep == False:
                ep = True
            elif lines.strip().startswith('#'):
                dict1['特效'] = lines.strip()[1:]
                ep, j = True, True
            elif lines.startswith('EX特性') or lines.startswith('插畫') or lines.startswith('聲優'):
                command, description = lines.strip().split("：")
                dict1[command] = description.strip()
                ep, j = True, True
            elif i > 3 and ep == False:
                ep1.append(lines.replace('[','').replace(']','').strip())
            elif ep == True and j == False:
                ep3.append(lines.replace('[','').replace(']','').strip())
            i = i + 1
        dict1['ep1'] = '\n'.join(ep1)
        if ''.join(ep3).strip() != '':
            dict1['ep3'] = '\n'.join(ep3)
        file.close()
        out_file = open(filepath.replace('.txt', '.json'), mode = 'w', encoding = 'utf8')
        json.dump(dict1, out_file, ensure_ascii = False, indent = 4, sort_keys = False)
        out_file.close()
