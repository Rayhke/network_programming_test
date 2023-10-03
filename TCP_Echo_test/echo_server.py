# socket 관련 패키지를 전부 가져 오겠다.
from socket import *

port = 8254
BUFSIZE = 1024

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('', port))
# 단, 한명만 연결을 받겠다.
sock.listen(1)
conn, (remotehost, remoteport) = sock.accept()
print('connected by', remotehost, remoteport)

while True:
    data = conn.recv(BUFSIZE)

    if not data:
        break

    print("Received message :", data.decode())
    conn.send(data)

conn.close()