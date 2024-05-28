import pyfiglet
import sys
import socket
from datetime import datetime
import threading
from queue import Queue
#Banner da ferramenta#
ascii_banner = pyfiglet.figlet_format("DUNKELHEIT")
print(ascii_banner)

#Input para digitar o IP do alvo
target = input(str("Target IP Address: "))

print("_" * 50)
print("Scanning IP: " + target)
print("Scanning started at: " + str(datetime.now()))
print("_" * 50)

#fila de portas
queue = Queue()

#funcao para escanear as portas e retornar os servicos utilizados
def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.5)
        result = s.connect_ex((target, port))
        if result == 0:
            service = ""
            if port == 20 or port == 21:
                service = "FTP"
            elif port == 22:
                service = "SSH"
            elif port == 25:
                service = "SMTP"
            elif port == 53:
                service = "DNS"
            elif port == 80:
                service = "HTTP"
            elif port == 179:
                service = "BGP"
            elif port == 443:
                service = "HTTPS"
            elif port == 587:
                service = "SMTPS"
            elif port == 3389:
                service = "RDP"

            if service: #se a porta estiver rodando um dos servicos acima, retorna a porta+servico
                print(f"\n[*] Port {port} ({service}) is open")
            else: #caso contrario apenas retorna a porta
                print(f"\n[*] Port {port} is open")
        s.close()
    except socket.error:
        print(f"\nCouldn't connect to server at port {port}")

#funcao threading
def threader():
    while True:
        worker = queue.get()
        scan_port(worker)
        queue.task_done()

#threading (utilizado para acelerar significativamente o scan das portas)
for x in range(100):  
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

#add as portas na fila
for port in range(1, 65535):
    queue.put(port)

queue.join()

print("_" * 50)
print("Scanning completed at: " + str(datetime.now()))
print("_" * 50)
