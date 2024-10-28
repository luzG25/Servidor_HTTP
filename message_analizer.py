def message_analiser(message):
    try:
        print(message)
        #message = message[(message.index('/')+1):(message.index('HTTP'))]
        for c in message:
            if '%20' in message:
                message = message.replace('%20', ' ')
        #print(message)
        if message.strip() == '':
            message = 'index.html'
        return message
    except:
        return ''

from time import sleep
print(message_analiser('file://desktop-243e7ar/Users/Gabriel%20da%20Luz/OneDrive/Documentos/Livros/Programa%C3%A7%C3%A3o/Machine%20Learning.pdf'))
  
