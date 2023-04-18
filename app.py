from flask import Flask, request, render_template
import random
import cv2
from pyzbar.pyzbar import decode
import socket

app = Flask(__name__)

app.static_folder = 'static'

templates = 'templates'

def comunicate(data: str):
    HOST = ''
    PORT = 23000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(data)
    socket_res = s.recv(1024)
    s.close()
    return socket_res

@app.route("/", methods=['GET'])
def root():
    return render_template("home.html")

@app.route("/manual", methods=['GET'])
def manual_display():
    return render_template("manual_display.html")

@app.route("/keypad/<type>", methods=['GET'])
def manual_display_keypad(type):
    return render_template("shared/keypad.html", header=type[0].upper() + type[1:])

@app.route("/acceso/<input>", methods=['GET'])
def acceso(input):
    granted = random.choice([True, False])
    parsed = input.split(",")
    img = cv2.imread("static/img/frame.png")
    qrData = decode(img)
    if len(qrData) > 0:
        binary = bin(int.from_bytes(qrData[0].data, byteorder='big'))
        print(binary)
    data = {
        "cel": parsed[0],
        "ci": parsed[1],
        "pin": parsed[2],
        "x": random.choice([0, 1]),
        "MAC": "00:00:00:00:00:00",
        "XXX": "elemento XXX o formato pdf417/qr",
        "binary": binary
    }
    return render_template("acceso.html", granted=granted, data=data)