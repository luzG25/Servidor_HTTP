raw_message = 'GET /favicon.ico HTTP/1.1\r\nHost: 192.168.43.24\r\nConnection: keep-alive\r\nUser-Agent: Mozilla/5.0 (Linux; Android 6.0; 4034X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.96 Mobile Safari/537.36\r\nAccept: image/webp,image/apng,image/*,*/*;q=0.8\r\nReferer: http://192.168.43.24/\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7\r\n\r\n'
raw_message2 = 'GET / HTTP/1.1\r\nHost: 192.168.43.24\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Linux; Android 6.0; 4034X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.96 Mobile Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7\r\n\r\n'

request = {'date': '', 'op': '', 'Host': '', 'Connection': '', 'User-Agent': '',
'Accept': '', 'Referer': '', 'Accept-Encoding': '', 'Accept-Language': '',
'Range': '', 'If-Modified_Since': ''}

request['op'] = raw_message[0:raw_message.index('\r\n')]
raw_message = raw_message[raw_message.index('\r\n')+2:]
print(raw_message)
while True:
    if '\n' in raw_message and ':' in raw_message:
        key = raw_message[:raw_message.index(':')]
        raw_message = raw_message[raw_message.index(':')+1:]
        request[key.strip()] = (raw_message[:raw_message.index('\r\n')]).strip()
        raw_message = raw_message[raw_message.index('\r\n')+2:]

    else:
        break
        
print(request)
