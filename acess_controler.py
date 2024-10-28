from json import load, dump
from os import listdir

def loader(dir, mode=''):
    file = open(dir,'r', encoding='utf-8' )
    if mode == 'json':
        content = load(file)
    else: 
        content = file.read()
    file.close()
    return content

def acess_controler(dirs_list, dir, mod='all'):
    dir = dir.strip()
    print(dir in dirs_list['premitido'])
    if mod == 'all':
        return dir

    elif dir in dirs_list['premitido'] and mod == 'controlado':
        return dir
    
    elif dir in dirs_list['proibido'] and mod == 'controlado':
        return '401 Unauthorized'

    elif (dir not in dirs_list['proibido']  and mod == 'premitivo') or (dir in dirs_list['premitido'] and mod == 'restritivo'):
        return dir
    
    elif (dir not in dirs_list['premitido'] and mod == 'restritivo') or (dir in dirs_list['proibido'] and mod == 'premitivo'):
        return '401 UNAUTHORIZED'
    else:
        return '404 NOT FOUND'

def dirs_searcher_engine(list, dir=''):
    if dir == '':
        list1 = listdir()
        for c in list1:
            if '.' not in c:
                #list.append((dir + c + '/'))
                dirs_searcher_engine(list, (dir + c + '/'))
            else:
                list.append((dir + c))
                
    else:
        list1 = listdir(dir)
        for c in list1:
            if '.' not in c:
                #list.append((dir + c + '/'))
                dirs_searcher_engine(list, (dir + c + '/'))
            else:
                list.append((dir + c))

def dirs_searcher():
    list = []
    dirs_searcher_engine(list)
    return list


def json_document_style(dir):
    file = open(dir, 'rb')
    content = file.read().decode()
    file.close()
    content1 = content
    n = -1
    l_c = 0
    c_c = 0
    for c in content1:
        n += 1
        if c == '{':
            content = content[:n+1] + '\n\t' + content[n+1:]
            n += 2

        elif c == ':':
            content = content[:n+1] + '\n\t\t' + content[n+1:]
            n += 2

        elif c == ',' and content[n-1:n] == ']':
            content = content[:n+1] + '\n\t' + content[n+1:]
            n += 2
        
        elif c == '}':
            content = content[:n] + '\n' + content[n:]
            n += 1

        elif c == '[':
            l_c = 1
        elif c == ']':
            l_c = 0

        elif l_c == 1 and c == ',':
            c_c += 1
            if c_c == 5:
                content = content[:n+1] + '\n\t\t' + content[n+1:]
                c_c = 0
                n += 2

    file = open(dir, 'wb')
    file.write(content.encode())
    file.close()

def update_list(dir, mode):
    if mode == 'premitivo':
        mode = 'premitido'
    else:
        mode = 'proibido'
    
    list = loader(dir, 'json')
    list[mode] = dirs_searcher()
    
    file = open(dir, 'w', encoding='utf-8')
    dump(list, file)

    json_document_style(dir)
