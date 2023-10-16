import cv2
import socket
import threading
import tkinter as tk
from UI import VideoChatUI
from PIL import Image, ImageTk


class VideoChatServer:
    def __init__(self):
        self.ui = VideoChatUI(tk.Tk(), "화상 채팅 서버")      # UI.py 연결
        self.ui.on_send_message = self.send_message_to_clients
        self.clients = []

        # 웹캠 초기화
        self.cap = cv2.VideoCapture(0)

        # 소켓 초기화
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 2458))
        self.server_socket.listen(5)

        # 웹캠 영상 전송 스레드 시작
        self.webcam_thread = threading.Thread(target=self.send_webcam)
        self.webcam_thread.daemon = True
        self.webcam_thread.start()

        # 클라이언트 연결을 처리하는 스레드 시작
        self.receive_thread = threading.Thread(target=self.receive_clients)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        # 서버 GUI 시작
        tk.mainloop()

    def show_frame(self, frame):
        self.ui.show_frame(frame)

    def send_message_to_clients(self, message):
        for client in self.clients:
            client.send(message.encode())
        # 서버 UI에도 메세지 표시

        self.ui.receive_message("서버 : " + message)

    def send_message_to_server(self, message):
        self.ui.receive_message(message)        # 서버에서 받은 메세지를 UI에 표시
        self.send_message_to_clients(message)   # 받은 메세지를 다른 클라이언트들에게 전송

    def send_webcam(self):
        while True:
            ret, frame = self.cap.read()
            # 색깔이 이상하게 나오는 원인
            # 원래 정상적으론 RGB 순서로 색상의 값을 주지만
            # 특이하게 BGR 순으로 값이 출력된 탓에 R값과 B값이 서로 바뀌어서 출력된 문제인 것.
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            if not ret:
                continue
            _, encoded_frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            encoded_frame = encoded_frame.tobytes()
            for client in self.clients:
                try:
                    client.send(encoded_frame)
                except:
                    self.clients.remove(client)
            # 서버 UI에도 비디오 화면 표시
            self.show_frame(frame)

    def handle_client(self, client_socket):
        self.clients.append(client_socket)
        while True:
            try:
                message = client_socket.recv(262144).decode()
                if not message:
                    self.clients.remove(client_socket)
                    client_socket.close()
                    break
                self.send_message_to_server(message)    # 클라이언트에서 받은 메세지를 서버로 전송
            except:
                pass

    def receive_clients(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.daemon = True
            client_handler.start()


if __name__ == "__main__":
    server = VideoChatServer()