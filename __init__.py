from webhook_tester.memory_database import Database
from webhook_tester.server import HttpServer
from webhook_tester.hooksocket import SocketServer, SocketClient
import os
import time

def __main__():
    print ("Creating empty database")
    db = Database()
    print ("Starting http server")
    try:
        port = int(os.env.get('HTTPSERVERPORT'))
    except:
        port = 9999
    srvr = HttpServer(host = os.env.get('HTTPSERVERHOST') or "",
                      port = port,
                      database = db)
    srvr.start()
    try:
        portsock = os.env.get('SOCKETSERVERPORT')
    except:
        portsock = 1337
    print ("Starting socket server")
    socketsrvr = SocketServer(host = os.env.get('SOCKETSERVERHOST') or "",
                              port = 1337,
                              database = db)
    socketsrvr.start()
    #time.sleep(5)
    #print ("Starting socket client for a small test")
    #socketclienttest = SocketClient(host = "localhost", port=1337)
    #result = socketclienttest.invoke(request = dict(method = "get",
    #                                                url = "http://google.com",
    #                                                data = dict()))
    #print(result)
