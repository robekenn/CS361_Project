import zmq
import json

context = zmq.Context()

def getData():
    
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    request = [1, "user_001"]
    serialized_request = json.dumps(request).encode('utf-8')

    print(f"Sending request: {request}")
    socket.send(serialized_request)

    response = socket.recv()
    socket.close()

    return json.loads(response)

def pushData(data):
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    request = [2, "user_001", data]
    serialized_request = json.dumps(request).encode('utf-8')

    socket.send(serialized_request)
    response = socket.recv()

    socket.close()

    return response