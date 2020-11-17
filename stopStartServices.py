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
def getService():
    service = None
    try:
        service = psutil.win_service_get(nomeServico)
        service = service.as_dict()
    except Exception as ex:
        print(str(ex))
    return service

#função que vai fazer o serviço parar e subir novamente
def stopStartService():
  #captura a hora atual do computador
  now = datetime.now()
  #se a hora for 23 e o minuto for 59
  if ( now.hour == 23 and now.minute == 59):
    #o computador vai ser reiniciado, você pode desligar o computador substituindo o /r por /s
    os.system("shutdown /r /t 1")
  
  #se nao for 23:59 chama a função para capturar as informações do serviço
  service = getService()

  if service:
      print("service found")
  else:
      print("service not found")

  #se o serviço estiver rodando ele vai estopar o srviço
  if service and service['status'] == 'running':
    # stop the service
    args = ['sc', 'stop', nomeServico]
    result = subprocess.run(args)
    #para a execução do codigo por 10 segundos para dar tempo do windows parar o serviço
    time.sleep(10)
    #sobe o serviço novamente
    args = ['sc', 'start', nomeServico]
    result = subprocess.run(args)
  else:
    #se o serviço não estiver rodando, ele vai iniciar o serviço
    print('Entrou Start')
    args = ['sc', 'start', nomeServico]
    result = subprocess.run(args)

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
    interval_monitor = setInterval(stopStartService, 3600)

