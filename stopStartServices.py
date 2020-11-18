import os
import subprocess
import time
import threading
import psutil 
from threading import Timer
from datetime import datetime

"""
precisa instalar o psutil, para isso precisa:
executar este comando no cmder: python -m pip install psutil
"""

nomeServico= 'Nome do Serviço'

#Busca as informações do serviço e retorna elas
def serviceGet():
    servico = None
    try:
        servico = psutil.win_service_get(nomeServico)
        servico = servico.as_dict()
    except Exception as ex:
        print(str(ex))
    return servico

#função que vai fazer o serviço parar e subir novamente
def stopStartService():
  #chama função para gravar log de execução do programa
  logExecucao()
  #captura a hora atual do computador
  horaAtual = datetime.now()
  #se a hora for 23 e o minuto for 59
  if ( horaAtual.hour == 23 and horaAtual.minute == 59):
    #o computador vai ser reiniciado, você pode desligar o computador substituindo o /r por /s
    os.system("shutdown /r /t 1")
  
  #se nao for 23:59 chama a função para capturar as informações do serviço
  servico = serviceGet()
  #se o serviço estiver rodando ele vai estopar o srviço
  if servico and servico['status'] == 'running':
    #para o serviço
    args = ['sc', 'stop', nomeServico]
    executa = subprocess.run(args)
    #para a execução do codigo por 10 segundos para dar tempo do windows parar o serviço
    time.sleep(10)
    #sobe o serviço novamente
    args = ['sc', 'start', nomeServico]
    executa = subprocess.run(args)
  else:
    #se o serviço não estiver rodando, ele vai iniciar o serviço
    args = ['sc', 'start', nomeServico]
    executa = subprocess.run(args)
    
def logExecucao():
    #captura o horário atual
    dateTimeObj = datetime.now()
    #formata o horário
    stringNow = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)")
    #procura o arquivo
    nomeArquivo = ('nome do seu arquivo de log')
    #abre o arquivo para leitura
    arquivo = open(nomeArquivo, "r")
    #le todas as linhas do programa e grava numa strig
    txtArq = arquivo.readlines()
    #grava na string uma linha nova com o horário atual
    txtArq.append('\n Última Leitura: ' + stringNow)
    #abre o arquivo para a leitura
    arquivo = open(nomeArquivo, 'w')
    #grava no arquivo a string
    arquivo.writelines(txtArq)
    #fecha o arquivo
    arquivo.close()

    return()

def defineIntervalo(function, interval, *params, **kwparams):
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
    #aqui você define, em segundos, quanto em quanto tempo seu script vai rodar, nesse caso o script roda uma vez a cada 3600 segundos
    interval_monitor = defineIntervalo(stopStartService, 3600)

