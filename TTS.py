import zmq
import json

context = zmq.Context()

def create_and_play(text):
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5554")
    siReq = [1, text]
    socket.send(json.dumps(siReq).encode('utf-8'))
    message = socket.recv()
    socket.close()
    return message.decode('utf-8')
