import zmq
import json

context = zmq.Context()

def add_points(amount):
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")

    siReq = [2, "user_001", amount]
    serialized_list_json = json.dumps(siReq).encode('utf-8')

    # send to the server
    socket.send(serialized_list_json)

    #receive responce
    message = socket.recv()
    socket.close()
    return message

def get_points():
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")

    siReq = [1, "user_001"]
    serialized_list_json = json.dumps(siReq).encode('utf-8')

    # send to the server
    socket.send(serialized_list_json)


    #receive responce
    message = socket.recv()
    socket.close()
    return message