#opções:
f_mode = 'premitivo'
port = 80
dir_flist = 'database.json'
servername = b'Goluz'
defs = {'main_url':'musica.html'}
####

import socket
from threading import Thread
from time import sleep as sl
from json import load
from acess_controler import acess_controler, loader, update_list

ip = socket.gethostbyname(socket.gethostname())
print(ip, ':', port)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((ip, port))
server.listen(5)

update_list(dir_flist, f_mode)
dir_list = loader(dir_flist, 'json')
print('Dados de locais premitidas e proibidas carregados!')

def type_analizer(message, defs):
    message = message.strip()
    #typ = message[(message.index('.')+1):].strip()
    typ = message[len(message)-4:]
    if '.' in typ:
        typ = typ[1:]
        if '.' in typ:
            typ = typ[1:]
    char = 'charset=UTF-8'
    types = {'html':('text/html;', char), 'png':('image/png;', ''), 'js':('aplication/javascript;', char),
         'ico':('image/ico;', ''), 'jpg':('image/jpg;',  ''), 'jpeg':('image/jpeg;',  ''), 'css':('text/css;', char),
         'mp3':('audio/mp3;', ''), 'mp4':('video/mp4;', ''), 'gif':('image/gif;', ''), 'mkv':('video/mkv;', ''),
         'pdf':('application/pdf;', ''), 'json':('', '')}
    return types[typ]


def file_sender(file_name, client, defs):
    file_content = b''
    if file_name in ('401 UNAUTHORIZED', '404 NOT FOUND'):
        content = b'HTTP/1.1 ' + file_name.encode() + b'\r\nDate: Fri, 17 Jul 2020 18:35:34 GMT\r\nServer:'+ servername + b'\r\n\r\n' 
    else:
        try:
            file = open(file_name, 'rb')
            file_content = file.read()
            file.close()
            typ = type_analizer(file_name, defs)
            head = b'HTTP/1.1 200 OK\r\nDate: Fri, 17 Jul 2020 18:35:34 GMT\r\nServer:'+ servername + b'\r\nLast-Modified: Thu, 12 Nov 2015 19:12:19 GMT\r\nAccept-Ranges: bytes\r\nContent-Length: ' + str(len(file_content)).encode() + b'\r\nVary: Accept-Encoding\r\nConnection: close\r\nContent-Type: ' + typ[0].encode() + typ[1].encode() + b'\r\n\r\n' 
        
        except:
            head = b'HTTP/1.1 404 Not Found\r\nDate: Fri, 17 Jul 2020 18:35:34 GMT\r\nServer:'+ servername + b'\r\n\r\n'

        content = (head + file_content)
            
    client.send(content)
    print('Enviado!')

def message_analiser(raw_message, defs):
    try:
        print(raw_message)
        request = {'date': '', 'op': '', 'Host': '', 'Connection': '', 'User-Agent': '',
        'Accept': '', 'Referer': '', 'Accept-Encoding': '', 'Accept-Language': '',
        'Range': '', 'If-Modified_Since': ''}
        
        request['op'] = raw_message[0:raw_message.index('\r\n')]
        raw_message = raw_message[raw_message.index('\r\n')+2:]
        while True:
            if '\n' in raw_message and ':' in raw_message:
                key = raw_message[:raw_message.index(':')]
                raw_message = raw_message[raw_message.index(':')+1:]
                request[key.strip()] = (raw_message[:raw_message.index('\r\n')]).strip()
                raw_message = raw_message[raw_message.index('\r\n')+2:]

            else:
                break
        del raw_message

        url = request['op']
        op = url[:url.index('/')]
        if 'GET' in op:
            url = url[url.index('/')+1:url.index('HTTP')]
            while '%20' in url:
                url = url.replace('%20', ' ')
            #print(url)
            if url.strip() == '':
                url = defs['main_url']
                
            del op
            file_sender(acess_controler(dir_list, url, f_mode), client, defs)
            
    except:
        print('error')


def clientHandling(client, defs):
    while True:
        message = client.recv(200000).decode()
        if message != '':
            Thread(target=message_analiser, args=(message,defs,)).start()
            #Thread(target=file_sender, args=(acess_controler(dir_list, message_analiser(message), f_mode), client,)).start()
            print('=' * 100)
  
while True:
    client, addr = server.accept()
    print(addr[0], ':', addr[1])
    Thread(target=clientHandling, args=(client, defs,)).start()
    #message = client.recv(200000).decode()
    
    #print('=' * 10)
