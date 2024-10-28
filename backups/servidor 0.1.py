#opções:
f_mode = 'premitivo'
port = 80
dir_flist = 'database.json'
servername = 'Goluz'
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

def type_analizer(message):
    message = message.strip()
    #typ = message[(message.index('.')+1):].strip()
    typ = message[len(message)-3:]
    char = 'charset=UTF-8'
    types = {'html':('text/html;', char), 'png':('image/png;', ''), 'js':('aplication/javascript;', char),
         'ico':('image/ico;', ''), 'jpg':('image/jpg;',  ''), 'jpeg':('image/jpeg;',  ''), 'css':('text/css;', char),
         'mp3':('audio/mp3;', ''), 'mp4':('video/mp4;', ''), 'gif':('image/gif;', ''), 'mkv':('video/mkv;', ''),
         'pdf':('application/pdf;', ''), 'json':('', '')}
    return types[typ]


def file_sender(file_name, client):
    if file_name in ('401 UNAUTHORIZED', '404 NOT FOUND'):
        content = b'HTTP/1.1 ' + file_name.encode() + b'\r\nDate: Fri, 17 Jul 2020 18:35:34 GMT\r\nServer:'+ servername.encode() + b'\r\n\r\n' 
    else:
        try:
            file = open(file_name, 'rb')
            file_content = file.read()
            file.close()
        except:
            content = b'HTTP/1.1 404 Not Found\r\nDate: Fri, 17 Jul 2020 18:35:34 GMT\r\nServer:'+ servername.encode() + b'\r\n\r\n'
        finally:
            typ = type_analizer(file_name)
            head = b'HTTP/1.1 200 OK\r\nDate: Fri, 17 Jul 2020 18:35:34 GMT\r\nServer:'+ servername.encode() + b'\r\nLast-Modified: Thu, 12 Nov 2015 19:12:19 GMT\r\nAccept-Ranges: bytes\r\nContent-Length: ' + str(len(file_content)).encode() + b'\r\nVary: Accept-Encoding\r\nConnection: close\r\nContent-Type: ' + typ[0].encode() + typ[1].encode() + b'\r\n\r\n' 
            content = (head + file_content)
    client.send(content)
    print('Enviado!')

def message_analiser(message):
    try:
        print(message)
        message = message[(message.index('/')+1):(message.index('HTTP'))]
        for c in message:
            if '%20' in message:
                message = message.replace('%20', ' ')
        #print(message)
        if message.strip() == '':
            message = 'index.html'
        return message
    except:
        return ''

def clientHandling(client):
    while True:
        message = client.recv(200000).decode()
        if message != '':
            Thread(target=file_sender, args=(acess_controler(dir_list, message_analiser(message), f_mode), client,)).start()
            print('=' * 100)
        

while True:
    client, addr = server.accept()
    print(addr[0], ':', addr[1])
    Thread(target=clientHandling, args=(client,)).start()
    #message = client.recv(200000).decode()
    
    #print('=' * 10)
