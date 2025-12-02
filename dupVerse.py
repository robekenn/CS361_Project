import zmq
import json

def deduplicate_verses_by_reference(verses):
    """
    Removes duplicate verses by reference using your microservice.
    verses: list of dicts [{"reference":..., "text":...}, ...]
    """
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5560")

    # Send to server
    request = [1, verses]
    socket.send(json.dumps(request).encode('utf-8'))

    # Receive deduplicated list
    unique_verses = json.loads(socket.recv().decode('utf-8'))
    socket.close()

    return unique_verses
