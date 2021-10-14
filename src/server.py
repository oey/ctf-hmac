#!/usr/bin/env python3

import socket, re
import hmac, hashlib

HOST = '' 
PORT = 31337        # Port to listen on (non-privileged ports are > 1023)

errorMessage = "Expected <message>;<auth> not ".encode()
publicKnownKey = "ourSharedSecret".encode()
privateKey = "898953458989753457348979534879 plus Port to listen on (non-privileged ports are > 1023)".encode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break

            elements = re.split(";", data.decode('utf-8').strip())
            
            if len(elements) == 2:
                receivedMessage = elements[0]
                receivedHmac = elements[1].lower()
                messageHmac = hmac.new(publicKnownKey, receivedMessage.encode(), hashlib.sha256).hexdigest().lower()
                taskHmac = hmac.new(privateKey, receivedMessage.encode(), hashlib.sha256).hexdigest().lower()
                print(f"hmac('{publicKnownKey}','{receivedMessage.encode()}') = {messageHmac}")
                if receivedHmac == messageHmac:         
                    print(f"{receivedMessage} and {receivedHmac} are authenticated")           
                    conn.sendall("200 OK\n".encode())
                    conn.sendall(b"Your knowledge about HMAC is verified.\n")
                    conn.sendall(b"The following line can be used for proof of completed task.\n")
                    conn.sendall(f"{receivedMessage};{taskHmac}\n".encode())
                elif receivedHmac == taskHmac:
                    print(f"verified: {receivedMessage} and {receivedHmac} are authenticated") 
                    conn.sendall("200 OK\n".encode())
                    conn.sendall(b"The message below is authenticated and valid.\n")
                    conn.sendall(f"{receivedMessage}\n".encode())
                else:
                    conn.sendall(f"401 Unauthorized {receivedMessage}\n".encode())
            else:         
                conn.sendall(errorMessage)
                conn.sendall(data)
                conn.sendall(b"\n")