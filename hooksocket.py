import socket
import sys
import json
import requests
import time
import threading

class SocketClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    def invoke(self, request):
        # Create a TCP/IP socket
        assert request.get('method') is not None
        assert request.get('url') is not None
        assert request.get('data') is not None
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        server_address = (self.host, self.port)
        print('connecting to {} port {}'.format(*server_address))
        sock.connect(server_address)
        result = dict()
        try:
            # Send data
            message = json.dumps(request)
            print(f'Sending message to SOCKET server: {message}')
            sock.sendall(bytes(message, 'utf-8'))

            # Look for the response
            print('Waiting result from SOCKET server')
            is_valid = False
            data = ""
            instructions = dict()
            while not is_valid:
                data += sock.recv(4096).decode('utf-8')
                try:
                    instructions = json.loads(data)
                    is_valid = True
                except:
                    is_valid = False
            result = instructions
        finally:
            print('closing CLIENT socket')
            sock.close()
        print(f'Result from SOCKET server: {json.dumps(result)}')
        return result


class SocketServer:
    def __init__(self, host, port, database):
        self.host = host
        self.port = port
        self.database = database

    def start(self):
        x = threading.Thread(target=self.__run)
        return x.start()

    def __run(self):
        print(f"Starting the SOCKET server @{self.host}:{self.port}")
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        server_address = (self.host, self.port)
        print('starting up on {} port {}'.format(*server_address))
        sock.bind(server_address)
        # Listen for incoming connections
        print("SOCKET server started.")
        sock.listen(1)
        while True:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = sock.accept()
            try:
                print('connection from', client_address)
                # Receive the data in small chunks and retransmit it
                is_valid = False
                instructions = dict()
                data = ""
                while not is_valid:
                    data += connection.recv(4096).decode('utf-8')
                    try:
                        instructions = json.loads(data)
                        is_valid = True
                    except:
                        is_valid = False
                print (json.dumps(instructions))
                #now we got some instructions, do them
                #read tye type of request: post or get
                #read the url of the request
                #read the body of the request
                #send the request
                params = dict(url = instructions['url'],
                             data = instructions['data'] or dict())
                result = getattr(requests, instructions['method'])(**params)
                #wait for the hook to speak to us
                hook = self.database.pop_all()
                while hook == []:
                    time.sleep(1)
                    hook = self.database.pop_all()
                #send the information of the hook to the client
                backfire = dict(result = dict(status_code = result.status_code,
                                              text = result.text,
                                              url = result.url),
                                hook = hook)
                print (dir(result))
                connection.sendall(bytes(json.dumps(backfire), 'utf-8'))
            except:
                raise Exception
            finally:
                # Clean up the connection
                print("SOCKET server closed.")
                connection.close()
