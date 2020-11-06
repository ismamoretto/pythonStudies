import imaplib
import email
import smtplib
from email.mime.text import MIMEText

#lembre de configurar o gmail para permitir a leitura de e-mails
FROM_EMAIL = "seuemail@gmail.com" 
FROM_PWD = "senhaEmail"
TO_ADDRS = ['email_destino@gmail.com'] #email destino
#configuração para enviar email
SMTP_SSL_HOST = 'smtp.gmail.com'# padrão
SMTP_SSL_PORT = 465# padrão
#configuração para receber e-mail
SMTP_SERVER = "imap.gmail.com"  # padrão
SMTP_PORT = 993  # padrão


def read_email():
    try:
        #Abre umaa conexão com o servidor e efetua o login.
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        
        #Em mail.select seleciono a caixa de e-mail que quero fazer a leitura, 
        #nesse caso, utilizei “inbox” para leitura dos e-mails. Ao final vamos atribuir um label aos e-mails pra isso passamos o parâmetro readonly=False.
        mail.select('inbox', readonly=False)
        
        #pesquisa por e-mail (TO), substituir o email para fazer a pesquisa, para usar é só descomentar a linha a baixo e comentar a pesquisa por assunto
        #type_mail, data = mail.search(None, 'TO "sendemail@gmail.com"')

        #pesquisa por assunto
        type_mail, data = mail.search(None, 'SUBJECT "Teste de leitura de email"')
        mail_ids = data[0]
        
        #aqui nós pegamos o primeiro e o último email para percorrermos cada deles.
        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        print("Reading emails from {} to {}.\n\n".format(latest_email_id, first_email_id))

        #Vamos usar mail.fetch com o protocolo RFC822 para obter os detalhes de cada e-mail,
        # i é o ID de cada email que estamos lendo
        for i in range(latest_email_id, first_email_id-1, -1):
            typ, data = mail.fetch(str.encode(str(i)), '(RFC822)')
            
            for response_part in data:
                if not isinstance(response_part, tuple):
                    continue
               
                #Aqui nós obtemos os detalhes do e-mail como assunto e remetente.
                msg = email.message_from_string(response_part[1].decode('utf-8'))
                email_subject = msg['subject']
                email_from = msg['from']
               
                #O conteúdo pode vir em texto puro ou multipart, se for texto puro vai direto para o else e extrair o conteúdo
                #senao tem que extrair somente o que precisa
                if msg.is_multipart():
                    mail_content = ''
                    for part in msg.get_payload():
                      if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    mail_content = msg.get_payload()
                    
                #usaremos MIMEText para enviar somente texto
                message = MIMEText(mail_content)
                message['subject'] = email_subject #Assunto do nosso email
                message['from'] = email_from #destino do nosso email
                message['to'] = ', '.join(TO_ADDRS) #endereço de quem esta enviando o email
                
                # Vamos conectar de forma segura, para isso uasaremos SSL
                server = smtplib.SMTP_SSL(SMTP_SSL_HOST, SMTP_SSL_PORT)
                
                #Fazendo login e enviando o e-mail
                server.login(FROM_EMAIL, FROM_PWD)
                server.sendmail(FROM_EMAIL, TO_ADDRS, message.as_string())
                
                #chama nossa função de log enviando o e-mail que geramos
                logScript(mail_content)
                    
                #para mostrar o resultado da leitura de emails descomentar as linhas a baixo
                #aqui imprimimos o conteúdo
                #print('From : ' + email_from + '\n')
                #print('Subject : ' + email_subject + '\n')
                #print('Content: {}'.format(mail_content))
                
                #Aqui é onde é feito a adição do label ao e-mail, substitua label-email
                mail.store(str.encode(str(i)), '+X-GM-LABELS', 'label-email')
                print('-------FIM-LEITURA-E-MAIL-----------------')

        mail.logout()

    except Exception as e:
        print(e)

#função que recebe um parametro e imprime ele no final de um arquivo de log
def logScript(corpoEmail):
    #pega o horário atual
    dateTimeObj = datetime.now()
    #transforma em string e no formato dia/ano e horario da execução
    stringNow = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)")
    
    #define o nome do arquivo
    nomeArquivo = ('Log.txt')
    #abre ele para leitura
    arquivo = open(nomeArquivo, "r")
    #le todos as linhas do arquivo
    txtArq = arquivo.readlines()
    #colocamos o horário que o log foi gerado
    txtArq.append('\n Horário Log: ' + stringNow +'\n')
    #adiciona nosso log
    txtArq.append(corpoEmail)
    #abre o arquivo para gravação
    arquivo = open(nomeArquivo, 'w')
    #grava o nosso log no arquivo
    arquivo.writelines(txtArq)
    #fecha o arquivo
    arquivo.close()

    return()

#Fução para fazer o script rodar de tempo em tempo
def setInterval(function, interval, *params, **kwparams):
    def setTimer(wrapper):
        wrapper.timer = Timer(interval, wrapper)
        wrapper.timer.start()

    def wrapper():
        function(*params, **kwparams)
        setTimer(wrapper)
    
    setTimer(wrapper)
    return wrapper

def clearInterval(wrapper):
    wrapper.timer.cancel()

if __name__ == '__main__':
    #faz o script rodar a cada 120seg
    interval_monitor = setInterval(read_email, 120)
