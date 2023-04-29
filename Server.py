#!/usr/bin/env python3
import socket
import numpy as np
import json
import time
import random
import sys
import json
import matplotlib.pyplot as plt
# HOST = '192.168.1.2' # IP address 
# PORT = 2136 # Port to listen on (use ports > 1023)
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen(0)
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#     while True:
#         data = conn.recv(65536).decode('utf-8')
#         print('Received from socket server : ', data)

HOST, PORT = '192.168.1.2', 8002
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(0)
print("Starting server at: ", (HOST, PORT))

raw_data = []
filtered_data = []

print('Waiting for new client')
Client, Addr = serverSocket.accept()
print('Connected by', Addr)
while True:

    try:
        Client.settimeout(5)
        data = Client.recv(4096).decode("utf-8")
        # print('Received from socket server : ', data)
        if len(raw_data) < 320 : raw_data += data.split()
        elif len(filtered_data) < 320 : filtered_data += data.split()

    except:
        Client.close()
        print('Timeout: client closed!')
        break

raw_data = [float(i) for i in raw_data]
filtered_data = [float(i) for i in filtered_data]
# print(len(raw_data), raw_data)
# print(len(filtered_data), filtered_data)

N = len(raw_data)
T = 1.0 / 100.0 #10ms
plt.subplot(2, 2, 1)
plt.plot(np.arange(0, 320), raw_data)
plt.title('raw data')
plt.xlabel('time (10ms)')
plt.ylabel('accelero z-axis (mg)')
y_f = np.fft.fft(raw_data)
x_f = np.linspace(0.0, 1.0/(2.0*T), N//2)
plt.subplot(2, 2, 2)
plt.plot(x_f, 2.0/N * np.abs(y_f[:N//2]))
plt.title('raw data (fft)')
plt.xlabel('frequency (Hz)')
# plt.plot(x_f, y[:N//2])
# print(y_f,len(y_f))

N = len(filtered_data)
T = 1.0 / 100.0 #10ms
plt.subplot(2, 2, 3)
plt.plot(np.arange(0, 320), filtered_data)
plt.title('filtered data')
plt.xlabel('time (10ms)')
y_f = np.fft.fft(filtered_data)
x_f = np.linspace(0.0, 1.0/(2.0*T), N//2)
plt.subplot(2, 2, 4)
plt.plot(x_f, 2.0/N * np.abs(y_f[:N//2]))
plt.title('filtered data (fft)')
plt.xlabel('frequency (Hz)')
#plt.plot(x_f, y[:N//2])
# print(y_f,len(y_f))
plt.show()