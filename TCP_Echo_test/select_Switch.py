from socket import *
from tkinter import *
from select import *
import time


def button_command():
    global sock, btn_text, btn_color
    if btn_text == 'ON':
        btn_text = 'OFF'
        btn_color = 'blue'
    else:
        btn_text = 'ON'
        btn_color = 'red'
    LED_button.configure(text=btn_text, bg=btn_color)
    sock.send(btn_text.encode())


root = Tk()         # 기본 윈도우 생성
btn_color = 'red'   # 버튼 색상
btn_text = 'ON'     # 버튼 텍스트

LED_label = Label(text="LED")          # LED 라벨
switch_label = Label(text="SWITCH")    # switch 라벨
switch_state_label = Label(text="Switch is OFF", fg='blue')
LED_button = Button(text=btn_text, fg="black", bg=btn_color,
                    command=button_command)
LED_label.grid(row=0, column=0)
LED_button.grid(row=0, column=1)
switch_label.grid(row=1, column=0)
switch_state_label.grid(row=1, column=1, sticky=E)

sock = socket()
sock.connect(('localhost', 2500))
mainloop()